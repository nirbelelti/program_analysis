import json

from graphviz import Digraph

json_data = open('car.json')


def create_uml_from_json(json_data):


    data = json.loads(json_data)
    print("data" + str(data))

    # Create a new Digraph
    dot = Digraph('UML Diagram', format='png')

    # Iterate through the classes in the JSON data
    for class_info in data:
        class_name = class_info['name']
        dot.node(class_name, class_name)

        # Add associations for superclasses
        for superclass in class_info.get('super', []):
            superclass_name = superclass['name']
            dot.edge(class_name, superclass_name)

    # Set the output file name and render the diagram
    output_file = 'uml_diagram'
    dot.render(output_file, format='png')


if __name__ == '__main__':
    # JSON data representing Java code metadata
    file = open('car.json')

    # returns JSON object as
    # a dictionary

    json_data = json.load(file)
    json_data = json.dumps(json_data)

    create_uml_from_json(str(json_data))
