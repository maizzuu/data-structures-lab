from calculatorIO import CalculatorIO

operators = {
    "+": {"precedence": 2, "associativity": "Left"},
    "-": {"precedence": 2, "associativity": "Left"},
    "*": {"precedence": 3, "associativity": "Left"},
    "/": {"precedence": 3, "associativity": "Left"},
    "^": {"precedence": 4, "associativity": "Right"}
}


class Calculator:
    """Class that uses the shunting-yard algorithm to turn
    an infix expression into a reverse polish one

    Attirbutes:
        io: class object for inputs and outputs
    """

    def __init__(self, io=CalculatorIO()):
        self.expression = ""
        self.output = []
        self.operators = []
        self.io = io

    def algorithm(self, expression):
        # type isn't needed until functions are included
        previous = {"input": "", "type": ""}
        for i, n in enumerate(expression):
            token = n
            next_token = expression[i+1] if i < (len(expression)-1) else None

            if token in "0123456789":
                if not next_token:
                    self.output.append(previous["input"] + token)
                elif next_token in "0123456789":
                    previous["input"] += token
                else:
                    self.output.append(previous["input"] + token)
                    previous["input"] = ""

            elif token in operators:
                if not self.operators:
                    self.operators.append(token)
                else:
                    while (
                        self.operators[-1] != "("
                        and ((operators[self.operators[-1]]["precedence"]
                              > operators[token]["precedence"])
                             or (operators[self.operators[-1]]["precedence"]
                             == operators[token]["precedence"]
                                 and operators[token]["associativity"] == "Left"))
                    ):
                        self.output.append(self.operators.pop())
                        if len(self.operators) == 0:
                            break
                    self.operators.append(token)
            elif token == "(":
                self.operators.append(token)
            elif token == ")":
                while True:
                    try:
                        top = self.operators.pop()
                    except IndexError:
                        self.io.write("ERROR: mismatched parentheses")
                        break
                    if top != "(":
                        self.output.append(top)
                        continue
                    break
        while self.operators:
            self.output.append(self.operators.pop())

    def start(self):
        while True:
            self.expression = self.io.read()
            print()
            if self.expression == "":
                self.io.write("Quitting calculator")
                break
            if self.expression == "help":
                self.io.write("instructions")
                print()
            else:
                self.algorithm(self.expression)
                self.io.write(" ".join(self.output))
                self.clear()

    def clear(self):
        self.output = []
        self.operators = []
