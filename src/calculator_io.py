class CalculatorIO:
    def read(self, text="Input"):
        input_str = input(f"{text}: ")
        return input_str

    def write(self, output):
        print(output)
        print()


calculator_io = CalculatorIO()
