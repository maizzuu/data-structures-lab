
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

    def __init__(self, expression: str):
        """The constructor for the ShuntingYard class.

        This constructor prepares the class for the parsing by creating empty lists and dict.

        Args:
            expression (str): The expression that will be parsed.
        """
        self.expression = expression
        self.output = []
        self.opstack = []
        # type isn't needed until functions are included
        self.previous = {"input": "", "type": ""}

    def parse(self) -> str:
        """Method that is in charge of parsing the expression and returning the final output.

        When the current token is a parenthesis, the method excepts
        an IndexError in case the parentheses are mismatched.

        Returns:
            str: The given expression in reverse polish notation.
        """

        for index, token in enumerate(self.expression):

            try:
                next_token = self.expression[index+1]
            except IndexError:
                next_token = None

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

            else:
                return "ERROR: invalid input"

        while self.opstack:
            if "(" in self.opstack or ")" in self.opstack:
                return "ERROR: mismatched parentheses"
            self.output.append(self.opstack.pop())
        return " ".join(self.output)

    # can't define the type of next_token because it fails the CI build
    def number(self, token: str, next_token: str | None):
        """_summary_

        Args:
            token (str): _description_
            next_token: _description_
        """
        if not next_token:
            self.output.append(self.previous["input"] + token)
        elif next_token in ".0123456789":
            self.previous["input"] += token
        else:
            self.output.append(self.previous["input"] + token)
            self.previous["input"] = ""

    def period(self, token: str, next_token, index: int):
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

        Args:
            token (str): The left or right parenthesis.
        """
        if token == "(":
            self.opstack.append(token)
        else:  # token == ")"
            while True:
                top = self.opstack.pop()
                if top != "(":
                    self.output.append(top)
                    continue
                break

    def check_adjacent_operators(self, token, next_token):
        if token in operators and next_token in operators:  # adjacent operators cause an error
            raise InputError

    def minus(self, token, previous_token):
        # if the previous token is a number this is an operation otherwise a negation
        if previous_token is None or previous_token not in "0123456789":
            self.previous["input"] += token
        else:
            self.operator(token)
