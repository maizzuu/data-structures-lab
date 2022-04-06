
operators = {
    "+": {"precedence": 2, "associativity": "Left"},
    "-": {"precedence": 2, "associativity": "Left"},
    "*": {"precedence": 3, "associativity": "Left"},
    "/": {"precedence": 3, "associativity": "Left"},
    "^": {"precedence": 4, "associativity": "Right"}
}


class InputError(Exception):
    pass


class ShuntingYard:
    """This class is used to parse an expression using the Shunting-yard algorithm.

    Infix notation -> RPN.

    Attributes:
        expression: The expression which will be parsed.
        output: A list that for storing the output as the algorithm parses the input.
        opstack: A list that is used to store operators.
        previous: A dictionary containing the previous character(s) and its type.
    """

    def __init__(self, expression: str, variables: dict):
        """The constructor for the ShuntingYard class.

        This constructor prepares the class for the parsing by creating empty lists and dict.

        Args:
            expression (str): The expression that will be parsed.
        """
        self.expression = expression
        self.variables = variables
        self.output = []
        self.opstack = []
        # type isn't needed until functions are included
        self.previous = {"input": "", "type": ""}

    def parse(self) -> str:
        """Method that is in charge of parsing the expression and returning the final output.

        This method will go through each token in the expression, check its type and
        handle it accordingly, also check the expression for any invalidities.

        Returns:
            str: The given expression in reverse polish notation.
        """

        for index, token in enumerate(self.expression):

            next_token = None if index == len(
                self.expression)-1 else self.expression[index+1]

            try:
                self.check_adjacent_operators(token, next_token)
            except InputError:
                return "ERROR: invalid input"

            if token in "0123456789":
                self.number(token, next_token)

            elif token == "-":  # special case of "-"" because it can also mean a negative number
                previous_token = None if index == 0 else self.expression[index-1]
                self.minus(token, previous_token)

            elif token == ".":
                try:
                    self.period(token, next_token, index)
                except InputError:
                    return "ERROR: invalid input"

            elif token in operators:
                self.operator(token)

            elif token in ("(", ")"):
                try:
                    self.parentheses(token)
                except IndexError:
                    return "ERROR: mismatched parentheses"

            elif token in self.variables:  # handle functions before this
                previous_token = None if index == 0 else self.expression[index-1]
                try:
                    self.variable(token, previous_token, next_token)
                except InputError:
                    return "ERROR: invalid input"

            else:
                return "ERROR: invalid input"

        try:
            self.finish()
        except InputError:
            return "ERROR: mismatched parentheses"

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
            self.output.append(self.previous["input"] + token)
        elif next_token in ".0123456789":
            self.previous["input"] += token
        else:
            self.output.append(self.previous["input"] + token)
            self.previous["input"] = ""

    def period(self, token: str, next_token, index: int):
        """A method for handling a period token.

        Will either raise an error or store the token in the case the next token is a number.

        Args:
            token (str): Current token, a period.
            next_token (str | None): The next token.
            index (int): The index of the current token.

        Raises:
            InputError: The first InputError will be raised if the expression starts with a period.
            InputError: The second InputError will be raised if next_token isn't a number.
        """
        if index == 0:
            raise InputError
        if not next_token or next_token not in "0123456789":
            raise InputError
        self.previous["input"] += token

    def operator(self, token: str):
        """A method for handling an operator token.

        Args:
            token (str): The operator.
        """
        if not self.opstack:
            self.opstack.append(token)
        else:
            while (
                self.opstack[-1] != "("
                and ((operators[self.opstack[-1]]["precedence"]
                      > operators[token]["precedence"])
                     or (operators[self.opstack[-1]]["precedence"]
                         == operators[token]["precedence"]
                         and operators[token]["associativity"] == "Left"))
            ):
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

    def check_adjacent_operators(self, token: str, next_token):
        """A method for checking whether an operator is followed by another one.

        Args:
            token (str): The current token.
            next_token (str | None): The next token.

        Raises:
            InputError: Error raised when token and next_token are both operators.
        """
        if token in operators and next_token in operators:  # adjacent operators cause an error
            raise InputError

    def minus(self, token: str, previous_token):
        """A method for handling a minus token.

        This method will check the type of the previous token to determine whether the
        minus sign is an operator or a negation.

        Args:
            token (str): The current token, a minus sign.
            previous_token (str | None): The previous token.
        """
        # if the previous token is a number this is an operation otherwise a negation
        if previous_token is None or previous_token not in "0123456789":
            self.previous["input"] += token
        else:
            self.operator(token)

    def finish(self):
        """A method for the final step of the Shunting-yard algorithm.

        This method will iterate through the remaining operator stack, checking whether
        any parentheses remain and adding operators to the output.

        Raises:
            InputError: Raised when there is a parenthesis left in the stack.
        """
        while self.opstack:
            if "(" in self.opstack or ")" in self.opstack:
                raise InputError
            self.output.append(self.opstack.pop())

    def variable(self, token: str, previous_token, next_token):
        if previous_token not in operators and previous_token is not None:
            raise InputError
        if next_token not in operators and next_token is not None:
            raise InputError
        value = self.variables[token]
        self.output.append(value)
