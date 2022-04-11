from math import cos, exp, log, sin, sqrt, tan
from shunting_yard import operators, functions


class Evaluator:
    """This class calculates the result of an equation in reverse Polish notation.

    Attributes:
        expression: The equation as a string.
        operands: An empty list for storing the operands.
    """

    def __init__(self, expression: str):
        """The constrcutor for this class.

        Args:
            expression (str): The equation as a string.
        """
        self.expression = expression.split(" ")
        self.operands = []

    def evaluate(self) -> int:
        """This method iterates the equation and is in charge of handling the tokens.

        Returns:
            int: Returns the final result of the equation.
        """
        if len(self.expression) == 1:
            return int(self.expression[0])
        for token in self.expression:
            if token in functions:
                x = self.operands.pop()
                result = self.function(token, x)
                self.operands.append(result)
            elif token in operators:
                second = self.operands.pop()
                first = self.operands.pop()
                result = self.calculate(token, first, second)
                self.operands.append(result)
            else:
                try:
                    self.operands.append(int(token))
                except ValueError:
                    self.operands.append(float(token))
        return self.operands.pop()

    def calculate(self, operator: str, first: int, second: int) -> int:
        """This method returns the result of one operation.

        Args:
            operator (str): The operation in question.
            first (int): The first operand.
            second (int): The second operand.

        Returns:
            int: The result of the operation.
        """
        if operator == "+":
            result = first + second
        elif operator == "-":
            result = first - second
        elif operator == "*":
            result = first * second
        elif operator == "/":
            result = first / second
        elif operator == "^":
            result = first ** second
        return round(result, 3)

    def function(self, name: str, x: int) -> int:
        if name == "cos":
            result = cos(x)
        elif name == "exp":
            result = exp(x)
        elif name == "lb":
            result = log(x, base=2)
        elif name == "lg":
            result = log(x, base=10)
        elif name == "ln":
            result = log(x)
        elif name == "sin":
            result = sin(x)
        elif name == "sqrt":
            result = sqrt(x)
        elif name == "tan":
            result = tan(x)
        return round(result, 3)
