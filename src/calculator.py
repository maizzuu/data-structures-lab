from calculatorIO import CalculatorIO
from shunting_yard import ShuntingYard


class Calculator:
    """Class that uses the shunting-yard algorithm to turn
    an infix expression into a reverse polish one

    Attirbutes:
        io: class object for inputs and outputs
    """

    def __init__(self, io=CalculatorIO()):
        self.io = io

    def algorithm(self, expression):
        pass

    def start(self):
        while True:
            expression = self.io.read()
            print()
            if expression == "":
                self.io.write("Quitting calculator")
                break
            if expression == "help":
                self.instructions()
            else:
                algorithm = ShuntingYard(expression)
                rpn = algorithm.parse()
                self.io.write(rpn)

    def instructions(self):
        self.io.write("instructions")
