from string import ascii_lowercase
from calculator_io import calculator_io as default_io
from shunting_yard import (InvalidInputError,
                           MismatchedParenthesesError,
                           ShuntingYard,
                           UnknownInputError)
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

    def __init__(self, io=default_io):
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
        interpreting the user input and giving it to the algorithm for parsing.
        """
        while True:
            expression = self.io.read(
                "Input an expression, empty to exit, help for instructions, var for variables")
            print()
            if expression == "":
                self.io.write("Quitting calculator")
                break
            if expression == "help":
                self.instructions()
            if expression == "var":
                self.variable_menu()
            else:
                try:
                    self.rpn = ShuntingYard(expression, self.variables).parse()
                    result = Evaluator(self.rpn).evaluate()
                    self.io.write(result)
                except InvalidInputError:
                    self.io.write("ERROR: invalid input")
                except UnknownInputError:
                    self.io.write("ERROR: unknown input")
                except IndexError:
                    self.io.write("ERROR: mismatched parentheses")
                except MismatchedParenthesesError:
                    self.io.write("ERROR: mismatched parentheses")

    def instructions(self):
        """Uses the IO to print out instructions for the calculator.
        """
        self.io.write("instructions")
        # instrcutions to be added:
        # use periods to indicate decimal places
        # type "var" to open the variable menu
        # var names can only include lowercase letters
        # var value can only be a number
        # functions must always be followed by a left parenthesis, i.e. "ln 2" is not ok

    def variable_menu(self):
        while True:
            input_str = self.io.read(
                "Input 'set', 'list', 'del' or empty to exit")

            if input_str == "":
                break

            if input_str == "list":
                for key, value in self.variables.items():
                    self.io.write(f"{key} = {value}")

            elif input_str == "set":
                self.set_variable()

            elif input_str == "del":
                name = self.io.read("Input variable name")
                try:
                    self.variables.pop(name)
                except KeyError:
                    self.io.write(f"Variable {name} not found")
            else:
                continue

    def check_var_name(self, name):
        for letter in name:
            if letter not in ascii_lowercase:
                return False
        return True

    def check_var_value(self, value):
        for index, token in enumerate(value):
            if token not in "0123456789":
                if token == "-" and index == 0:
                    continue
                return False
        return True

    def set_variable(self):
        while True:
            name = self.io.read("Input variable name")
            if self.check_var_name(name):
                break
        while True:
            value = self.io.read("Input variable value")
            if self.check_var_value(value):
                break
        if name == "" or value == "":
            return
        self.variables[name] = value
