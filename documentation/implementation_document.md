# Implementation document

## Project structure

Right now the project consists of four different classes:

- `CalculatorIO` is used to get user inputs and print outputs.
- `Calculator` is the base for the calculator. It also contains the methods for storing, listing and deleting variables.
- `ShuntingYard` contains the shunting-yard algorithm. It takes an infix expression as a parameter and returns it in reverse Polish notation.
- `Evaluator` calculates the final result of the expression.

`index.py` is used to start the calculator from the terminal, and all unit tests are in the `TestCalculator` class.

## Implemented time and space complexities

I implemented the algorithm according to this pseudocode from Wikipedia, however this pseudocode does not take into account numbers larger than 9, negative numbers or variables.
