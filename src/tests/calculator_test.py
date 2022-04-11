import unittest
from calculator import Calculator


class StubIO:
    def __init__(self, inputs: list):
        self.inputs = inputs
        self.outputs = []

    def read(self, text):  # attr text not needed
        return self.inputs.pop(0)

    def write(self, output):
        self.outputs.append(output)


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.io = StubIO([])
        self.calc = Calculator(self.io)

    def test_empty_expression_quits(self):
        self.io.inputs = [""]

        self.calc.start()

        self.assertEqual(self.io.outputs[0], "Quitting calculator")

    def test_input_help_for_instructions(self):
        # the last item in the input list must always be "" to stop the running
        self.io.inputs = ["help", ""]

        self.calc.start()

        self.assertEqual(self.io.outputs[0], "instructions")

    def test_correct_rpn_result_plus(self):
        self.io.inputs = ["5+2", ""]

        self.calc.start()

        self.assertEqual(self.calc.rpn, "5 2 +")
        self.assertEqual(self.io.outputs[0], 7)

    def test_correct_rpn_result_minus(self):
        self.io.inputs = ["7-2", ""]

        self.calc.start()

        self.assertEqual(self.calc.rpn, "7 2 -")
        self.assertEqual(self.io.outputs[0], 5)

    def test_correct_rpn_result_multiplication(self):
        self.io.inputs = ["3*2", ""]

        self.calc.start()

        self.assertEqual(self.calc.rpn, "3 2 *")
        self.assertEqual(self.io.outputs[0], 6)

    def test_correct_rpn_result_division(self):
        self.io.inputs = ["6/2", ""]

        self.calc.start()

        self.assertEqual(self.calc.rpn, "6 2 /")
        self.assertEqual(self.io.outputs[0], 3)

    def test_division_rounded_result_correct(self):
        self.io.inputs = ["100/3", ""]

        self.calc.start()

        self.assertEqual(self.io.outputs[0], 33.333)

    def test_correct_rpn_result_power(self):
        self.io.inputs = ["4^3", ""]

        self.calc.start()

        self.assertEqual(self.calc.rpn, "4 3 ^")
        self.assertEqual(self.io.outputs[0], 64)

    def test_input_len_1(self):
        self.io.inputs = ["2", ""]

        self.calc.start()

        self.assertEqual(self.calc.rpn, "2")
        self.assertEqual(self.io.outputs[0], 2)

    def test_mismatched_parentheses_error(self):
        self.io.inputs = ["2*4-5)", ""]

        self.calc.start()

        self.assertEqual(self.io.outputs[0], "ERROR: mismatched parentheses")

    def test_input_with_decimal(self):
        self.io.inputs = ["3.5*2", ""]

        self.calc.start()

        self.assertEqual(self.calc.rpn, "3.5 2 *")
        self.assertEqual(self.io.outputs[0], 7)

    def test_expression_ends_in_period_error(self):
        self.io.inputs = ["4*6+5.", ""]

        self.calc.start()

        self.assertEqual(self.io.outputs[0], "ERROR: invalid input")

    def test_expression_starts_with_period(self):
        self.io.inputs = [".6+5", ""]

        self.calc.start()

        self.assertEqual(self.io.outputs[0], "ERROR: invalid input")

    def test_invalid_input(self):
        self.io.inputs = ["4€+3", ""]

        self.calc.start()

        self.assertEqual(self.io.outputs[0], "ERROR: invalid input")

    def test_parentheses(self):
        self.io.inputs = ["3*(4+6)^3-(2+1)*4", ""]

        self.calc.start()

        self.assertEqual(self.calc.rpn, "3 4 6 + 3 ^ * 2 1 + 4 * -")
        self.assertEqual(self.io.outputs[0], 2988)

    def test_mismatched_parenthesis_at_end(self):
        self.io.inputs = ["3*(4+8)(", ""]

        self.calc.start()

        self.assertEqual(self.io.outputs[0], "ERROR: mismatched parentheses")

    def test_adjacent_operators(self):
        self.io.inputs = ["3*/5", ""]

        self.calc.start()

        self.assertEqual(self.io.outputs[0], "ERROR: invalid input")

    def test_negative_number_first(self):
        self.io.inputs = ["-5+6", ""]

        self.calc.start()

        self.assertEqual(self.calc.rpn, "-5 6 +")
        self.assertEqual(self.io.outputs[0], 1)

    def test_negative_number_in_parentheses(self):
        self.io.inputs = ["4*(-4+8)", ""]

        self.calc.start()

        self.assertEqual(self.calc.rpn, "4 -4 8 + *")
        self.assertEqual(self.io.outputs[0], 16)

    def test_variable_menu_exit(self):
        self.io.inputs = ["var", "", ""]

        self.calc.start()

        self.assertEqual(
            self.io.outputs[0], "Quitting calculator")

    def test_set_variable(self):
        self.io.inputs = ["var", "set", "a", "5", "", ""]

        self.calc.start()

        self.assertEqual(self.calc.variables, {"a": "5"})

    def test_set_invalid_variable_name_and_value(self):
        self.io.inputs = ["var", "set", "aaaa", "4", "a", "5r", "5", "", ""]

        self.calc.start()

        self.assertEqual(self.calc.variables, {"a": "5"})

    def test_list_variables(self):
        self.io.inputs = ["var", "list", "", ""]

        self.calc.variables = {"a": 5, "b": 100}
        self.calc.start()

        self.assertEqual(self.io.outputs[0], "a = 5")
        self.assertEqual(self.io.outputs[1], "b = 100")

    def test_set_negative_variable_value(self):
        self.io.inputs = ["var", "set", "a", "-5", "", ""]

        self.calc.start()

        self.assertEqual(self.calc.variables, {"a": "-5"})

    def test_delete_variable(self):
        self.io.inputs = ["var", "del", "a", "", ""]

        self.calc.variables = {"a": "6"}
        self.calc.start()

        self.assertEqual(self.calc.variables, {})

    def test_delete_nonexistent_variable(self):
        self.io.inputs = ["var", "del", "a", "", ""]

        self.calc.start()

        self.assertEqual(self.io.outputs[0], "Variable a not found")

    def test_unknown_var_command(self):
        self.io.inputs = ["var", "se", "set", "a", "5" "", "", ""]

        self.calc.start()

        self.assertEqual(self.calc.variables, {"a": "5"})

    def test_variable_in_algorithm(self):
        self.io.inputs = ["3+a", ""]

        self.calc.variables = {"a": "5"}
        self.calc.start()

        self.assertEqual(self.calc.rpn, "3 5 +")
        self.assertEqual(self.io.outputs[0], 8)

    def test_invalid_input_with_variable(self):
        self.io.inputs = ["a3-4", "3a-4", ""]

        self.calc.variables = {"a": "5"}
        self.calc.start()

        self.assertEqual(self.io.outputs[0], "ERROR: invalid input")
        self.assertEqual(self.io.outputs[1], "ERROR: invalid input")
