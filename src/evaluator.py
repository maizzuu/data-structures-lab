from shunting_yard import operators


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
            if token not in operators:
                try:
                    self.operands.append(int(token))
                except ValueError:
                    self.operands.append(float(token))
            else:
                second = self.operands.pop()
                first = self.operands.pop()
                result = self.calculate(token, first, second)
                self.operands.append(result)
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
            return first + second
        if operator == "-":
            return first - second
        if operator == "*":
            return first * second
        if operator == "/":
            return round(first / second, 3)
        return first ** second  # if operator == "^"
