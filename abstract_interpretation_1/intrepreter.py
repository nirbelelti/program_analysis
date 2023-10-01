import glob
import json
import pathlib
import subprocess


class Comparison:
    @staticmethod
    def is_greater(a, b):
        return a > b

    @staticmethod
    def is_greater_or_equal(a, b):
        return a >= b

    @staticmethod
    def is_less_or_equal(a, b):
        return a <= b


class ArithmeticOperation:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def divide(a, b):
        return a // b

    @staticmethod
    def modulo(a, b):
        return a % b


class JavaMethod:
    @staticmethod
    def get_field_type(field_dict):
        valid_dict = {
            "class": "java/lang/System",
            "name": "out",
            "type": {
                "kind": "class",
                "name": "java/io/PrintStream"
            }
        }
        return field_dict.get("type", {}).get("name") if field_dict == valid_dict else None

    @staticmethod
    def print_line(string):
        print(string)


class Interpreter:
    def __init__(self, program, verbose, avail_programs):
        self.program = program
        self.verbose = verbose
        self.avail_programs = avail_programs
        self.memory = []
        self.stack = []

    def run(self, f):
        self.stack.append(f)
        print("--- Starting execution... ---")
        while True:
            end_of_program, return_value = self.step()
            print("Stack: ", self.stack)
            print("Memory: ", self.memory)
            if return_value is not None:
                print(return_value)
                return return_value
            if end_of_program:
                break
        print('--- Done ---')
        return None

    def step(self):
        if not self.stack:
            return True, None
        (_, _, pc) = self.stack[-1]
        b = self.program['bytecode'][pc]
        if self.verbose:
            print("Starting...: ", b)
        if hasattr(self, "_"+b["opr"]):
            return False, getattr(self, "_"+b["opr"])(b)
        else:
            print("Unknown instruction: ", b)
            return True, None

    def _return(self, b):
        (_, os, _) = self.stack.pop(-1)
        if b["type"] is None:
            return None
        elif b["type"] == "int":
            return os[-1]

    def _push(self, b):
        (lv, os, pc) = self.stack.pop(-1)
        value = b["value"]
        self.stack.append((lv, os + [value["value"]], pc + 1))

    def _load(self, b):
        (lv, os, pc) = self.stack.pop(-1)
        if b["type"] == "ref":
            value = lv[b["index"]]
            self.stack.append((lv, os + [value], pc + 1))
        else:
            value = lv[b["index"]]
            self.stack.append((lv, os + [value], pc + 1))

    def _binary(self, b):
        (lv, os, pc) = self.stack.pop(-1)
        value = getattr(ArithmeticOperation, "_"+b["operant"])(os[-2], os[-1])
        self.stack.append((lv, os[:-2] + [value], pc + 1))

    def _if(self, b):
        (lv, os, pc) = self.stack.pop(-1)
        condition = getattr(Comparison, "_"+b["condition"])(os[-2], os[-1])
        if condition:
            pc = b["target"]
        else:
            pc = pc + 1
        self.stack.append((lv, os[:-2], pc))

    def _store(self, b):
        (lv, os, pc) = self.stack.pop(-1)
        value = os[-1]
        if b["index"] >= len(lv):
            lv = lv + [value]
        else:
            lv[b["index"]] = value
        self.stack.append((lv, os[:-1], pc + 1))

    def _incr(self, b):
        (lv, os, pc) = self.stack.pop(-1)
        lv[b["index"]] = lv[b["index"]] + b["amount"]
        self.stack.append((lv, os, pc + 1))

    def _ifz(self, b):
        (lv, os, pc) = self.stack.pop(-1)
        condition = getattr(Comparison, "_"+b["condition"])(os[-1], 0)
        if condition:
            pc = b["target"]
        else:
            pc = pc + 1
        self.stack.append((lv, os[:-1], pc))

    def _goto(self, b):
        (lv, os, pc) = self.stack.pop(-1)
        value = b["target"]
        pc = value
        self.stack.append((lv, os, pc))

    def _get(self, b):
        (lv, os, pc) = self.stack.pop(-1)
        value = getattr(JavaMethod, "_get")(b["field"])
        self.stack.append((lv, os + [value], pc + 1))

    def _invoke(self, b):
        (lv, os, pc) = self.stack.pop(-1)
        arg_num = len(b["method"]["args"])

        try:
            if hasattr(JavaMethod, "_" + b["method"]["name"]):
                if arg_num == 0:
                    value = getattr(JavaMethod, "_" + b["method"]["name"])([])
                else:
                    value = getattr(JavaMethod, "_" + b["method"]["name"])(*os[-arg_num:])
                if b["access"] != "dynamic":
                    if b["method"]["ref"]["name"] == os[-arg_num-1]:
                        self.stack.append((lv, os[:-arg_num-1] + [value], pc + 1))
                    else:
                        raise Exception
            else:
                raise Exception
        except:
            interpret = Interpreter(self.avail_programs[b["method"]["name"]], self.verbose, self.avail_programs)
            if arg_num == 0:
                (l_new, s_new, pc_new) = [], [], 0
            else:
                (l_new, s_new, pc_new) = os[-arg_num:], [], 0
            ret = interpret.run((l_new, s_new, pc_new))
            if b["method"]["returns"] is None:
                if arg_num == 0:
                    self.stack.append((lv, os, pc + 1))
                else:
                    self.stack.append((lv, os[:-arg_num], pc + 1))
            else:
                if arg_num == 0:
                    self.stack.append((lv, os + [ret], pc + 1))
                else:
                    self.stack.append((lv, os[:-arg_num] + [ret], pc + 1))

    def _array_load(self, b):
        (lv, os, pc) = self.stack.pop(-1)
        index_el = os[-1]
        index_array = os[-2]
        value = self.memory[index_array][index_el]
        self.stack.append((lv, os[:-2] + [value], pc + 1))

    def _array_store(self, b):
        (lv, os, pc) = self.stack.pop(-1)
        value = os[-1]
        index_of_array = os[-3]
        index_of_el = os[-2]
        if len(self.memory[index_of_array]) <= index_of_el:
            self.memory[index_of_array].append(value)
        else:
            self.memory[index_of_array][index_of_el] = value
        self.stack.append((lv, os[:-3], pc + 1))

    def _newarray(self, b):
        (lv, os, pc) = self.stack.pop(-1)
        self.memory.append([])
        self.stack.append((lv, os + [len(self.memory)-1], pc + 1))

    def _dup(self, b):
        (lv, os, pc) = self.stack.pop(-1)
        self.stack.append((lv, os + os[-b["words"]:], pc + 1))

    def _arraylength(self, b):
        (lv, os, pc) = self.stack.pop(-1)
        index_array = os[-1]
        value = len(self.memory[index_array])
        self.stack.append((lv, os[:-1] + [value], pc + 1))


class AbstractInterpreter:

    def __init__(self):
        pass

    def abstract_step(self, instruction, variables):
        opr = instruction.get('opr')
        errors = []

        if opr == 'load':
            index = instruction.get('index')
            value = instruction.get('value', None)  # get value from instruction, default to None if not provided
            variables[index] = {'type': instruction.get('type'), 'value': value}

        elif opr == 'binary' and instruction.get('operant') == 'div':
            divisor_index = instruction.get('index')
            if variables.get(divisor_index, {}).get('value') == 0:
                errors.append('ArithmeticException: Division by Zero')

        elif opr == 'invoke':
            ref = instruction.get('ref', {})
            if variables.get(ref.get('name'), None) is None:
                errors.append('NullPointerException: Null reference invocation')

        elif opr == 'throw' and instruction.get('class') == 'java/lang/UnsupportedOperationException':
            errors.append('UnsupportedOperationException: Unsupported operation')

        # Further abstraction steps for other operations and errors, e.g., IndexOutOfBoundsException

        return variables, errors

    def bounded_abstract_interpretation(self, bytecode, k):
        variables = {}
        all_errors = []
        for i in range(min(k, len(bytecode))):
            instruction = bytecode[i]
            variables, errors = self.abstract_step(instruction, variables)
            if errors:
                all_errors.extend(errors)

        return all_errors if all_errors else 'No Exception Found'


def get_function_bytecode(json_obj):
    return json_obj['code']


def get_functions(json_obj):
    functions = {}
    for func in json_obj['methods']:
        if any(anno['type'] == 'dtu/compute/exec/Case' for anno in func['annotations']):
            functions[func['name']] = get_function_bytecode(func)
    return functions


def analyse_bytecode(folder_path, target_folder_path):
    class_files = glob.glob(folder_path + '/**/*.class', recursive=True)
    for class_file in class_files:
        json_file = pathlib.Path(class_file).with_suffix('.json').name
        target_file = pathlib.Path(target_folder_path) / json_file
        command = ["jvm2json", "-s", class_file, "-t", str(target_file)]
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main():
    # folder_path = "../../course-02242-examples/src/executables/java/dtu/compute/exec"
    # target_folder_path = "../../course-02242-examples/decompiled/dtu/compute/exec/"
    # analyse_bytecode(folder_path, target_folder_path)

    file_path = "../decompiled/dtu/compute/exec/Array.json"
    with open(file_path, 'r') as file:
        json_obj = json.load(file)
        byte_codes = get_functions(json_obj)
        interpreter = AbstractInterpreter()
        for key, value in byte_codes.items():
            print('Case:', key)
            current_bc = value['bytecode']
            error = interpreter.bounded_abstract_interpretation(current_bc, len(current_bc))
            print('Has error:', error)


if __name__ == "__main__":
    main()
