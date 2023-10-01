import json


def interpret_function(data_dict):
    methods = list_of_methods(data_dict)
    for method in methods:
        # if (method == "noop" or method == "hundredAndTwo" or method == "<init>" or method == "zero"
        #         or method =="identity" or method=="add" or method == 'min' or method =="factorial"):  # At the moment we are limiting the methods to supported ones only
        print('Method:', method)
        data_stack = create_stack(method, data_dict)
        interpret_instruction(data_stack)


def list_of_methods(
        data_dict):  # Since we are incrementing our interpretation over various methods, it creates a list of methods.
    methods = []
    for obj in data_dict['methods']:
        methods.append(obj['name'])
    return methods


def create_stack(metod_name, data):
    stack = []
    for method in data["methods"]:
        if method["name"] == metod_name:
            selected_method = method
            break
    if selected_method['code'].get('bytecode'):
        for step in selected_method['code']['bytecode']:
            stack.append(step)
    return stack

class IndexOutOfBoundsException(Exception):
    def __str__(self):
        return "Index out of bounds."

class ArithmeticException(Exception):
    def __str__(self):
        return "Arithmetic error."

class NullPointerException(Exception):
    def __str__(self):
        return "Null pointer accessed."

class UnsupportedOperationException(Exception):
    def __str__(self):
        return "Operation is not supported."

class UnsupportedValueTypeError(Exception):
    def __str__(self):
        return "Unsupported value type."

class InvalidInstructionError(Exception):
    def __str__(self):
        return "Invalid instruction encountered."

class InvalidOffsetError(Exception):
    def __str__(self):
        return "Invalid offset provided."


def interpret_instruction(stack):
    for instruction in stack:
        opr = instruction.get('opr', None)
        offset = instruction.get('offset', None)
        

        if opr == 'return':
            print(f'Interpreting return instruction at offset {offset}')
            print('Returning from the current method')
            
        elif opr == 'binary':
            print(f'Interpreting binary operation at offset {offset}')
            operant = instruction.get('operant', None)
            if operant == "div" and stack[-1] == 0:  # Assuming that the top of the stack is the divisor
                raise ArithmeticException("Division by zero.")
            print(f'Performing binary operation: {operant}')

        elif opr == 'load':
            index = instruction.get('index', None)
            if index is None or index < 0 or index >= len(stack):
                raise IndexOutOfBoundsException(f"Invalid index {index} at offset {offset}")
            print(f'Loading reference from index: {index}')

            if not stack[index]:
                raise NullPointerException(f"Null reference at index {index} and offset {offset}")


        elif opr == 'push':
            value = instruction.get('value', None)
            value_type = value.get('type', None) if value else None
            if value_type == 'integer':
                print(f'Interpreting push instruction at offset {offset}')
                print(f'Pushing integer value: {value["value"]}')
            else:
                raise UnsupportedValueTypeError(f"Unsupported value type: {value_type} at offset {offset}")
            
        elif opr == 'incr':
            print(f'Interpreting increment instruction at offset {offset}')
            index = instruction['index']
            amount = instruction['amount']
            print(f'Incrementing value at index {index} by {amount}')

        elif opr == 'store':
            print(f'Interpreting store instruction at offset {offset}')
            index = instruction.get('index', None)
            print(f'Storing value to index: {index}')

        elif opr == 'invoke':
            print(f'Interpreting invoke instruction at offset {offset}')
            method = instruction.get('method', None)
            if not method:
                raise InvalidInstructionError(f"Method details missing for invoke instruction at offset {offset}")
            method_name = method.get('name', None)
            method_ref = method.get('ref', None)
            is_interface = method.get('is_interface', None)
            print(f'Invoking method: {method_name}')
            print(f'Method reference: {method_ref}')
            print(f'Is interface: {is_interface}')


        elif opr in ['if', 'ifz']:
            print(f'Interpreting {opr} instruction at offset {offset}')
            condition = instruction.get('condition', None)
            target_offset = instruction.get('target', None)
            print(f'Condition: {condition}, Target Offset: {target_offset}')
            if condition in ['gt', 'le']:
                if instruction and (not target_offset or target_offset >= len(stack)):
                    raise InvalidOffsetError(f"Invalid target offset for jump at offset {offset}")

        elif opr == 'goto':
            print(f'Interpreting goto instruction at offset {offset}')
            target_offset = instruction.get('target', None)
            print(f'Jumping to offset {target_offset}')

        else:
            raise InvalidInstructionError(f"Unknown instruction: {instruction} at offset {offset}")


    print('--------------------------------------------')


if __name__ == '__main__':
    with open('Array.json', 'r') as f:
        data_dict = json.load(f)

    interpret_function(data_dict)


    
