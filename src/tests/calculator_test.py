import unittest
from calculator import Calculator


class StubIO:
    def __init__(self, inputs: list):
        self.inputs = inputs
        self.outputs = []

    def read(self):
        return self.inputs.pop(0)

    def write(self, output):
        self.outputs.append(output)


class TestCalculator(unittest.TestCase):
    def test_empty_expression_quits(self):
        io = StubIO([""])

        calc = Calculator(io)
        calc.start()

        self.assertEqual(io.outputs[0], "Quitting calculator")

    def test_input_help_for_instructions(self):
        # the last item in the input list must always be "" to stop the running
        io = StubIO(["help", ""])

        calc = Calculator(io)
        calc.start()

        self.assertEqual(io.outputs[0], "instructions")

    def test_algorithm_basic(self):
        io = StubIO(["12+3", ""])

        calc = Calculator(io)
        calc.start()

        self.assertEqual(io.outputs[0], "12 3 +")

    def test_algorithm_two_operations(self):
        io = StubIO(["1+2-3", ""])

        calc = Calculator(io)
        calc.start()

        self.assertEqual(io.outputs[0], "1 2 + 3 -")

    def test_algorithm_with_parentheses(self):
        io = StubIO(["2*(3-2)", ""])

        calc = Calculator(io)
        calc.start()

        self.assertEqual(io.outputs[0], "2 3 2 - *")

    def test_mismatched_parentheses_cause_an_error(self):
        io = StubIO(["2*()))", ""])

        calc = Calculator(io)
        calc.start()

        self.assertEqual(io.outputs[0], "ERROR: mismatched parentheses")

    def test_algorithm_iterates_stack(self):
        io = StubIO(["3*4*(2+5)", ""])

        calc = Calculator(io)
        calc.start()

        self.assertEqual(io.outputs[0], "3 4 * 2 5 + *")

    def test_algorithm_long_expression(self):
        io = StubIO(["1*(4+5)^8+5+(8-4)*5", ""])

        calc = Calculator(io)
        calc.start()

        self.assertEqual(io.outputs[0], "1 4 5 + 8 ^ * 5 + 8 4 - 5 * +")

    def test_unknown_input(self):
        io = StubIO(["1+2€", ""])

        calc = Calculator(io)
        calc.start()

        self.assertEqual(io.outputs[0], "ERROR: unknown input")
