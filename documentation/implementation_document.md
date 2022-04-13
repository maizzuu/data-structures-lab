# Implementation document

## Project structure

Right now the project consists of four different classes:

- `CalculatorIO` is used to get user inputs and print outputs.
- `Calculator` is the base for the calculator. It also contains the methods for storing, listing and deleting variables.
- `ShuntingYard` contains the shunting-yard algorithm. It takes an infix expression as a parameter and returns it in reverse Polish notation.
- `Evaluator` calculates the final result of the expression.

`index.py` is used to start the calculator from the terminal, and all unit tests under the `tests` directory.

## Implemented time and space complexities

I implemented the algorithm according to this pseudocode from Wikipedia, however this pseudocode does not take into account numbers larger than 9, negative numbers or variables.
<img width="997" alt="Screenshot 2022-04-07 at 10 58 50" src="https://user-images.githubusercontent.com/80681082/162150998-c011085a-adf3-4510-9460-cccbcc868a9b.png">

The time complexity is O(n), where n is the length of the expression. The space complexity is also O(n) because of the output list.

## Possible flaws and improvements

The calculator should work with all kinds of inputs but it is very much possible that I have not tested a certain kind of input that won't work.

## Sources

The screenshot of the pseudocode is from [this](https://en.wikipedia.org/wiki/Shunting-yard_algorithm#The_algorithm_in_detail) Wikipedia article.
