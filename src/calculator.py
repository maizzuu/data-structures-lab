operators = {
    "+": {"precedence":2, "associativity":"Left"},
    "-": {"precedence":2, "associativity":"Left"},
    "*": {"precedence":3, "associativity":"Left"},
    "/": {"precedence":3, "associativity":"Left"},
    "^": {"precedence":4, "associativity":"Right"}
}

class Calculator:
    def __init__ (self):
        self.expression = ""
        self.output = ""
        self.operators = []

    def algorithm(self,expression):
        previous = {"input": "", "type": ""}
        for i in range(0, len(expression)):
            token = expression[i]
            next = expression[i+1]

            if token in "0123456789":
                if next in "0123456789":
                    previous["input"] += token
                else:
                    input = previous["input"] + token
                    output += input
            
            elif token in operators:
                top = self.operators[-1]
                while (
                    top != "(" 
                    and ((operators[top]["precedence"] > operators[token]["presedence"]) 
                    or (operators[top]["presedence"] == operators[token]["presedence"] 
                    and operators[token]["associativity"] == "Left"))
                ):
                    output =+ self.operators.pop()
                self.operators.append(token)
            elif token == "(":
                self.operators.append(token)
            
    def start(self):
        while True:
            print("Input an expression to calculate, leave empty to exit, help for instructions")
            self.expression = input("Input:")
            print()
            if self.expression == "":
                break
            elif self.expression == "help":
                print("***INSERT INSTRUCTIONS HERE***")
                print()
            else:
                self.algorithm(self.expression)
            # TODO handle output and calculate answer