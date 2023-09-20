import unittest
import json
from interpretation import list_of_methods, create_stack   # Import the methods to be tested


class TestInterpreterMethods(unittest.TestCase):

    def test_list_of_methods(self):
        # Sample data dictionary similar to the one used for interpretation
        with open('Simple.json', 'r') as f:
            data_dict = json.load(f)

        # Call the method to get the list of method names
        result = list_of_methods(data_dict)

        # Assert that the result matches the expected list of method names
        expected_result = ['<init>', 'noop', 'zero', 'hundredAndTwo', 'identity', 'add', 'min', 'factorial']
        self.assertEqual(result, expected_result)

    def test_create_stack(self):
        with open('Simple.json', 'r') as f:
            data_dict = json.load(f)

        # Call the method to create the stack for a given method
        result = create_stack("noop", data_dict)

        # Assert that the result matches the expected stack for "method1"
        expected_result = [{"offset": 0, "opr": "return", "type": None}]
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
