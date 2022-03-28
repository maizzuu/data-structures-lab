from shunting_yard import operators


class Evaluator:
    def __init__(self, expression: str):
        self.expression = expression.split(" ")
        self.operands = []

    def evaluate(self) -> int:
        if len(self.expression) == 1:
            return int(self.expression[0])
        for token in self.expression:
            if token not in operators:
                self.operands.append(int(token))
            else:
                second = self.operands.pop()
                first = self.operands.pop()
                result = self.calculate(token, first, second)
                self.operands.append(result)
        return self.operands.pop()

    def calculate(self, operator: str, first: int, second: int) -> int:
        if operator == "+":
            return first + second
        if operator == "-":
            return first - second
        if operator == "*":
            return first * second
        if operator == "/":
            return first / second
        if operator == "^":
            return first ** second
