import unittest
from calculator import Calculator


class StubIO:
    def __init__(self):
        self.inputs = []
        self.outputs = []

    def read(self, text=""):
        return self.inputs.pop(0)

    def write(self, output):
        self.outputs.append(output)

    def set_inputs(self, inputs: list):
        self.inputs = inputs + ["", ""]


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.io = StubIO()
        self.calc = Calculator(self.io)

    def test_empty_expression_quits(self):
        self.io.set_inputs([""])

        self.calc.start()

        self.assertEqual(self.io.outputs[0], "Quitting calculator")

    def test_input_help_for_instructions(self):
        # the last item in the input list must always be "" to stop the running
        self.io.set_inputs(["help"])

        self.calc.start()

        self.assertEqual(self.io.outputs[0], "instructions")

    def test_set_variable(self):
        self.io.set_inputs(["var", "set", "a", "5"])

        self.calc.start()

        self.assertEqual(self.calc.variables, {"a": "5"})

    def test_list_variables(self):
        self.io.set_inputs(["var", "set", "a", "5", "list"])
        self.calc.variables = {"b": "3"}

        self.calc.start()

        self.assertEqual(self.io.outputs[0:2], ["b = 3", "a = 5"])

    def test_invalid_var_name_and_value(self):
        self.io.set_inputs(["var", "set", "a!", "a", "3€", "3"])

        self.calc.start()

        self.assertEqual(self.calc.variables, {"a": "3"})

    def test_empty_name_or_value_does_nothing(self):
        self.io.set_inputs(["var", "set", "", ""])

        self.calc.start()

        self.assertEqual(self.calc.variables, {})

    def test_negative_var_value(self):
        self.io.set_inputs(["var", "set", "a", "-5"])

        self.calc.start()

        self.assertEqual(self.calc.variables, {"a": "-5"})

    def test_del_var_correct_name(self):
        self.io.set_inputs(["var", "del", "a"])
        self.calc.variables = {"a": "5", "beta": "3"}

        self.calc.start()

        self.assertEqual(self.calc.variables, {"beta": "3"})

    def test_del_var_invalid_name(self):
        self.io.set_inputs(["var", "del", "a"])
        self.calc.variables = {"alpha": "5", "beta": "3"}

        self.calc.start()

        self.assertEqual(self.io.outputs[0], "Variable a not found")

    def test_var_menu_unknown_input_does_nothing(self):
        self.io.set_inputs(["var", "llist", "list"])
        self.calc.variables = {"alpha": "5", "beta": "3"}

        self.calc.start()

        self.assertEqual(self.io.outputs[1], "beta = 3")
