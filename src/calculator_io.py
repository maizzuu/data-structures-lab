instructions = [
    "Use periods to indicate decimal places",
    "Trigonometric functions use radians",
    "Variable names can only include lowercase letters",
    "Variable value can only be a number",
    "Functions must always be followed by a left parenthesis, i.e. 'ln 2' is not ok"]


class CalculatorIO:
    def read(self, text="Input"):
        input_str = input(f"{text}: ")
        return input_str

    def write(self, output):
        print(output)
        print()

    def print_instructions(self):
        for item in instructions:
            print(item)
        print()


calculator_io = CalculatorIO()
