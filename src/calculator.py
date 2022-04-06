from string import ascii_lowercase
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
            rpn: Stores the RPN version of the expression. (Only for testing purposes.)
        """
        self.io = io
        self.rpn = ""
        self.variables = {}

    def start(self):
        """Starts the calculator and is in charge of running it.

        Is also in charge of asking the IO for inputs and giving it outputs, as well as
        interpreting the user input and giving it for the algorithm for parsing.
        """
        while True:
            self.io.write(
                "Input an expression or leave empty to exit, type help for instructions")
            expression = self.io.read()
            print()
            if expression == "":
                self.io.write("Quitting calculator")
                break
            if expression == "help":
                self.instructions()
            if expression == "var":
                self.variable_menu()
            else:
                # a new instance created for each expression
                self.rpn = ShuntingYard(expression, self.variables).parse()
                try:
                    result = Evaluator(self.rpn).evaluate()
                    self.io.write(result)
                except ValueError:  # for when rpn is actually an error message
                    self.io.write(self.rpn)

    def instructions(self):
        """Uses the IO to print out instructions for the calculator.
        """
        self.io.write("instructions")
        # instrcutions to be added:
        # use periods to indicate decimal places
        # type "var" to open the variable menu
        # var names can only include lowercase letters
        # var name max len is 1
        # var value can only be a number

    def variable_menu(self):
        while True:
            self.io.write(
                """Type 'set' to set a variable, 'list' to list all variables,
                'del' to remove one, leave empty to return""")
            input_str = self.io.read()

            if input_str == "":
                break

            elif input_str == "list":
                for key, value in self.variables.items():
                    print(f"{key} = {value}")

            elif input_str == "set":
                while True:
                    self.io.write("Input variable name")
                    name = self.io.read()
                    if self.check_var_name(name):
                        break
                while True:
                    self.io.write("Input variable value")
                    value = self.io.read()
                    if self.check_var_value(value):
                        break
                self.variables[name] = value

            elif input_str == "del":
                self.io.write("Input variable name")
                name = self.io.read()
                try:
                    self.variables.pop(name)
                except KeyError:
                    self.io.write(f"Variable name {name} not found")

    def check_var_name(self, name):
        if len(name) != 1:
            return False
        if name not in ascii_lowercase:
            return False
        return True

    def check_var_value(self, value):
        for index, token in enumerate(value):
            if token not in "0123456789":
                if token == "-" and index == 0:
                    continue
                return False
        return True
