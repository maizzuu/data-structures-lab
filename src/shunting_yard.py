from types import NoneType


operators = {
    "+": {"precedence": 2, "associativity": "Left"},
    "-": {"precedence": 2, "associativity": "Left"},
    "*": {"precedence": 3, "associativity": "Left"},
    "/": {"precedence": 3, "associativity": "Left"},
    "^": {"precedence": 4, "associativity": "Right"}
}


class ShuntingYard:
    def __init__(self, expression: str):
        self.expression = expression
        self.output = []
        self.opstack = []
        # type isn't needed until functions are included
        self.previous = {"input": "", "type": ""}

    def parse(self):

        for index, token in enumerate(self.expression):
            try:
                next_token = self.expression[index+1]
            except IndexError:
                next_token = None

            if token in "0123456789":
                self.number(token, next_token)

            elif token in operators:
                self.operator(token)

            elif token in ("(", ")"):
                try:
                    self.parentheses(token)
                except IndexError:
                    return "ERROR: mismatched parentheses"
            else:
                return "ERROR: unknown input"

        while self.opstack:
            self.output.append(self.opstack.pop())
        return " ".join(self.output)

    def number(self, token: str, next_token: str | NoneType):
        if not next_token:
            self.output.append(self.previous["input"] + token)
        elif next_token in "0123456789":
            self.previous["input"] += token
        else:
            self.output.append(self.previous["input"] + token)
            self.previous["input"] = ""

    def operator(self, token: str):
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
        if token == "(":
            self.opstack.append(token)
        elif token == ")":
            while True:
                top = self.opstack.pop()
                if top != "(":
                    self.output.append(top)
                    continue
                break
