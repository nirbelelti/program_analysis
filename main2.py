import json

from graphviz import Digraph


def create_uml_from_json(data_list):
    # Create a new Digraph
    dot = Digraph('UML Diagram', format='png')

    for data in data_list:
        # Extract class details
        class_name = data["name"]

        # Build a label for the class with its attributes and methods
        label = class_name + "|"

        # Add attributes to the label
        for attribute in data["attributes"]:
            access_symbol = '+' if attribute["access"] == "public" else '-'
            label += f"{access_symbol} {attribute['name']} : {attribute['type']}\\l"

        # Add methods to the label
        label += "|"
        for method in data["methods"]:
            access_symbol = '+' if method["access"] == "public" else '-'
            param_list = ', '.join(
                [f"{param['name']} : {param['type']}" for param in method.get("params", [])])
            label += f"{access_symbol} {method['name']}({param_list}) : {method['returnType']}\\l"

        dot.node(class_name, label, shape='record')

        # Add relationships
        if "relations" in data:
            for relation in data["relations"]:
                if relation["type"] == "inheritance":
                    dot.edge(relation["target"], class_name)

    # Set the output file name and render the diagram
    output_file = 'uml_diagram'
    dot.render(output_file, format='png')
    print(f"Diagram saved as {output_file}.png")


if __name__ == '__main__':
    with open('car2.json', 'r') as f:
        data_list = json.load(f)

    create_uml_from_json(data_list)
