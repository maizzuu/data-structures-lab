from calculatorIO import CalculatorIO
from shunting_yard import ShuntingYard
from evaluator import Evaluator


class Calculator:
    """Class that is the framework for the calculator.

    This class is used to create an instance of the calculator and to start
    that calculator. It needs an IO attribute for getting user inputs and
    printing outputs. It will ask the user for an input via the IO module,
    and then give it to the algorithm module for parsing.

    Attributes:
        io: Class instance for inputs and outputs. The default value is of the CalculatorI0 class.
    """

    def __init__(self, io=CalculatorIO()):
        """The constructor for this class. It creates an instance of the IO-class.

        Args:
            io: Used for inputs and outputs. Defaults to CalculatorIO.
        """
        self.io = io

    def start(self):
        """Starts the calculator and is in charge of running it.

        Is also in charge of asking the IO for inputs and giving it outputs, as well as
        interpreting the user input and giving it for the algorithm for parsing.
        """
        while True:
            expression = self.io.read()
            print()
            if expression == "":
                self.io.write("Quitting calculator")
                break
            if expression == "help":
                self.instructions()
            else:
                # a new instance created for each expression
                rpn = ShuntingYard(expression).parse()
                result = Evaluator(rpn).evaluate()
                self.io.write(result)

    def instructions(self):
        """Uses the IO to print out instructions for the calculator.
        """
        self.io.write("instructions")
