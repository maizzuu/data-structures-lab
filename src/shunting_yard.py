
from string import ascii_lowercase


operators = ["+", "-", "*", "/", "^"]
functions = ["cos", "exp", "lb", "lg", "ln", "sin", "sqrt", "tan"]
precedence = {
    "+": 2,
    "-": 2,
    "*": 3,
    "/": 3,
    "^": 4
}

associativity = {
    "+": "Left",
    "-": "Left",
    "*": "Left",
    "/": "Left",
    "^": "Right"
}


class InvalidInputError(Exception):
    pass


class UnknownInputError(Exception):
    pass


class MismatchedParenthesesError(Exception):
    pass


class ShuntingYard:
    """This class is used to parse an expression using the Shunting-yard algorithm.

    Infix notation -> RPN.

    Attributes:
        expression: The expression which will be parsed.
        variables: The variables that have been set.
        output: A list that for storing the output as the algorithm parses the input.
        opstack: A list that is used to store operators.
        funcstack: A list that is used to store functions.
        previous: A string containing the previous character(s).
    """

    def __init__(self, expression: str, variables: dict):
        """The constructor for the ShuntingYard class.

        This constructor prepares the class for the parsing by creating empty lists and dict.

        Args:
            expression (str): The expression in infix notation.
            variables (dict): Variables currently stored.
        """
        self.expression = expression
        self.variables = variables
        self.output = []
        self.opstack = []
        self.funcstack = []
        self.previous = ""

    def parse(self) -> str:
        """Method that is in charge of parsing the expression and returning the final output.

        This method will go through each token in the expression, check its type and
        handle it accordingly, also check the expression for any invalidities.


        Raises:
            InvalidInputError: Raised when the expression contains an unsuitable character.

        Returns:
            str: The expression in postfix (reverse Polish) notation.
        """

        for index, token in enumerate(self.expression):

            next_token = None if index == len(
                self.expression)-1 else self.expression[index+1]
            previous_token = None if index == 0 else self.expression[index-1]

            self.check_adjacent_operators(token, next_token)

            if token in "0123456789":
                self.number(token, next_token)

            elif token == "-":  # special case of "-"" because it can also mean a negative number
                self.minus(token, previous_token, next_token)

            elif token == ".":
                self.period(token, next_token, index)

            elif token in operators:
                self.operator(token)

            elif token in ("(", ")"):
                self.parentheses(token)

            elif token in ascii_lowercase:
                self.letter(token, next_token, previous_token)

            else:
                raise InvalidInputError

        self.finish()

        return " ".join(self.output)

    # can't define the type of next_token here because it fails the CI build
    def number(self, token: str, next_token):
        """A method for handling a number token.

        The number will be stored if the next token is also a number,
        otherwise it will be added to the output.

        Args:
            token (str): Current token, a number.
            next_token(str | None): The next token.
        """
        if not next_token:
            self.output.append(self.previous + token)
        elif next_token in ".0123456789":
            self.previous += token
        else:
            self.output.append(self.previous + token)
            self.previous = ""

    def period(self, token: str, next_token, index: int):
        """A method for handling a period token.

        Will either raise an error or store the token in the case the next token is a number.

        Args:
            token (str): Current token, a period.
            next_token (str | None): The next token.
            index (int): The index of the current token.

        Raises:
            InvalidInputError: Will be raised if the expression starts with a period.
            InvalidInputError: Will be raised if next_token isn't a number.
        """
        if index == 0:
            raise InvalidInputError
        if not next_token or next_token not in "0123456789":
            raise InvalidInputError
        self.previous += token

    def operator(self, token: str):
        """A method for handling an operator token.

        Args:
            token (str): The operator.
        """
        if not self.opstack:
            self.opstack.append(token)
        else:
            while (self.opstack[-1] != "("
                   and ((precedence[self.opstack[-1]] > precedence[token])
                        or (precedence[self.opstack[-1]] == precedence[token]
                            and associativity[token] == "Left"))):
                self.output.append(self.opstack.pop())
                if len(self.opstack) == 0:
                    break
            self.opstack.append(token)

    def parentheses(self, token: str):
        """A method for handling a parenthesis token.

        All left parentheses will be added to the operator stack, while a right parenthesis will
        cause the iteration of the operator stack. If the top operator is a left parentheses, it
        will just be popped from the stack. While the top operator is something else, it is added
        to the output. If the stack is empty, an IndexError will be raised.

        Args:
            token (str): The left or right parenthesis.

        Raises:
            IndexError: Error raised when running out of operators looking for a left parenthesis.
        """
        if token == "(":
            self.opstack.append(token)
        else:  # token == ")"
            while True:
                if not self.opstack:
                    raise IndexError
                top = self.opstack.pop()
                if top != "(":
                    self.output.append(top)
                    continue
                break
            if self.funcstack:
                self.output.append(self.funcstack.pop())

    def check_adjacent_operators(self, token: str, next_token):
        """A method for checking whether an operator is followed by another one.

        Returns None if token is a parenthesis.

        Args:
            token (str): The current token.
            next_token (str | None): The next token.

        Raises:
            InvalidInputError: Error raised when token and next_token are both operators.
        """
        if token in operators and next_token in operators:  # adjacent operators cause an error
            raise InvalidInputError

    def minus(self, token: str, previous_token, next_token):
        """A method for handling a minus token.

        This method will check the type of the previous token to determine whether the
        minus sign is an operator or a negation.

        Args:
            token (str): The current token, a minus sign.
            previous_token (str | None): The previous token.
        """
        if previous_token is None and next_token == "(":
            self.output.append("0")
            self.operator(token)
        elif previous_token is None or previous_token not in "0123456789)":
            self.previous += token
        else:
            self.operator(token)

    def finish(self):
        """A method for the final step of the Shunting-yard algorithm.

        This method will iterate through the remaining operator stack, checking whether
        any parentheses remain and adding operators to the output.

        Raises:
            MismatchedParenthesesError: Raised when there is a parenthesis left in the stack.
        """
        while self.opstack:
            if "(" in self.opstack or ")" in self.opstack:
                raise MismatchedParenthesesError
            self.output.append(self.opstack.pop())

    def letter(self, token: str, next_token, previous_token):
        """Handles a letter based on what kind the preceding and following tokens are of.

        Args:
            token (str): The current token (a letter)
            next_token (str | None): The next token.
            previous_token (str | None): The previous token.

        Raises:
            UnknownInputError: When a variable with a certain name hasn't been set.
            InvalidInputError: A number precedes or follows a one-letter var.
            InvalidInputError: A number precedes a variable/function.
            InvalidInputError: A number follows a variable/function.
            InvalidInputError: The preceding or following token is not of one of the allowed types.
            UnknownInputError: _description_
        """
        # "+a+" (has to be a variable, no functions of length 1)
        if str(previous_token) not in ascii_lowercase and str(next_token) not in ascii_lowercase:
            if token not in self.variables:
                raise UnknownInputError
            if ((previous_token is not None and previous_token not in "+-*/^()")
                    or (next_token is not None and next_token not in "+-*/^()")):  # "3a"
                raise InvalidInputError
            value = self.variables[token]
            self.output.append(value)

        # "+ab"
        elif str(previous_token) not in ascii_lowercase and str(next_token) in ascii_lowercase:
            if previous_token is not None and previous_token not in "+-*/^()":
                raise InvalidInputError
            self.previous += token

        # "ab+"
        elif str(previous_token) in ascii_lowercase and str(next_token) not in ascii_lowercase:
            full_str = self.previous + token
            self.previous = ""
            if full_str in self.variables:
                if next_token is not None and next_token not in "+-*/^()":  # "ab3"
                    raise InvalidInputError
                value = self.variables[full_str]
                self.output.append(value)
            elif full_str in functions:
                if next_token != "(":  # "ln3" or "ln+"
                    raise InvalidInputError
                self.funcstack.append(full_str)
            else:
                raise UnknownInputError

        # "abc"
        # str(previous_token) in ascii_lowercase and str(next_token) in ascii_lowercase:
        else:
            self.previous += token


# if __name__ == "__main__":
