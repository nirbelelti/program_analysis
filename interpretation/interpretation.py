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


def interpret_instruction(stack):  # covarage
    for instruction in stack:
        opr = instruction['opr']
        offset = instruction['offset']

        if opr == 'return':  # noop
            print(f'Interpreting return instruction at offset {offset}')
            # Perform the return operation based on the context of your program
            # In this example, we'll print a message to indicate the return operation
            print('Returning from the current method')

        elif opr == 'push':  # code
            value = instruction['value']
            value_type = value['type']
            if value_type == 'integer':
                print(f'Interpreting push instruction at offset {offset}')
                print(f'Pushing integer value: {value["value"]}')
            else:
                print(f'Interpreting push instruction at offset {offset}')
                print(f'Unsupported value type: {value_type}')

        elif opr == 'load':  # <init>
            print(f'Interpreting load instruction at offset {offset}')
            index = instruction['index']
            print(f'Loading reference from index: {index}')

        elif opr == 'store':
            print(f'Interpreting store instruction at offset {offset}')
            index = instruction['index']
            print(f'Storing value to index: {index}')

        elif opr == 'invoke':  # <init>
            print(f'Interpreting invoke instruction at offset {offset}')
            method = instruction['method']
            method_name = method['name']
            method_ref = method['ref']
            is_interface = method['is_interface']
            print(f'Invoking method: {method_name}')
            print(f'Method reference: {method_ref}')
            print(f'Is interface: {is_interface}')

        elif opr == 'binary':
            print(f'Interpreting binary operation at offset {offset}')
            operant = instruction['operant']
            print(f'Performing binary operation: {operant}')

        elif opr == 'if':
            print(f'Interpreting if instruction at offset {offset}')
            condition = instruction['condition']
            target_offset = instruction['target']
            print(f'Condition: {condition}, Target Offset: {target_offset}')
            # Perform conditional jump based on the condition and target offset
            if condition == 'gt':
                if instruction and target_offset < len(instruction):
                    target_instruction = instruction[target_offset]
                    print(f'Jumping to offset {target_offset}, target instruction: {target_instruction}')
                else:
                    print('Invalid target offset for jump.')

        elif opr == 'incr':
            print(f'Interpreting increment instruction at offset {offset}')
            index = instruction['index']
            amount = instruction['amount']
            print(f'Incrementing value at index {index} by {amount}')

        elif opr == 'ifz':
            print(f'Interpreting if-zero instruction at offset {offset}')
            condition = instruction['condition']
            target_offset = instruction['target']
            print(f'Condition: {condition}, Target Offset: {target_offset}')
            if condition == 'le':
                if instruction and target_offset < len(instruction):
                    target_instruction = instruction[target_offset]
                    print(f'Jumping to offset {target_offset}, target instruction: {target_instruction}')
                else:
                    print('Invalid target offset for jump.')

        elif opr == 'goto':
            print(f'Interpreting goto instruction at offset {offset}')
            target_offset = instruction['target']
            print(f'Jumping to offset {target_offset}')

        else:
            print('Unknown instruction:', instruction)
    print('--------------------------------------------')


if __name__ == '__main__':
    with open('Simple.json', 'r') as f:
        data_dict = json.load(f)

    interpret_function(data_dict)
