class CalculatorIO:
    def read(self):
        print("Input an expression to calculate, leave empty to exit, help for instructions")
        input_str = input("Input: ")
        return input_str

    def write(self, output):
        print(output)
