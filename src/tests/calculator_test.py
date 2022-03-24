import unittest
from calculator import Calculator

class StubIO:
    def __init__(self, expression):
        self.expression = expression
        self.outputs = []

    def read(self):
        return self.expression

    def write(self, output):
        self.outputs.append(output)

class TestCalculator(unittest.TestCase):
    def test_empty_expression_quits(self):
        io = StubIO("")
        
        calc = Calculator(io)
        calc.start()

        self.assertEqual(io.outputs[0], "Quitting calculator")