import json
from graphviz import Digraph

json_data = open('car.json')
def create_uml_from_json(json_data):


    data = json.loads(json_data)
    print("data"+ str(data))

    # Create a new Digraph
    dot = Digraph('UML Diagram', format='png')

    # Iterate through the classes in the JSON data
    for class_info in data:
        class_name = class_info['name']
        dot.node(class_name, class_name)

        # Add associations for superclasses
        for superclass in class_info.get('super', []):
            superclass_name = superclass[0]
            dot.edge(class_name, superclass_name)

    # Set the output file name and render the diagram
    output_file = 'uml_diagram'
    dot.render(output_file, format='png')

if __name__ == '__main__':
    # JSON data representing Java code metadata
    json_data = '''
    [
        {
            "name": "Main",
            "access": ["public", "super"],
            "typeparams": [],
            "super": {
                "name": "java/lang/Object",
                "inner": null,
                "args": [],
                "annotations": []
            },
            "interfaces": [],
            "fields": [],
            "methods": [
                {
                    "name": "<init>",
                    "access": ["public"],
                    "typeparams": [],
                    "params": [],
                    "returns": {
                        "type": null,
                        "annotations": []
                    },
                    "annotations": [],
                    "exceptions": [],
                    "default": null
                }
            ],
            "annotations": [],
            "exceptions": [],
            "default": null
        }
    ]
    '''

    create_uml_from_json(json_data)
