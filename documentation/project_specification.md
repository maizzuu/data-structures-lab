# Project specification

This program is a scientific calculator that uses the [shunting-yard](https://en.wikipedia.org/wiki/Shunting-yard_algorithm) algorithm to turn an expression into a [Reverse Polish Notation](https://en.wikipedia.org/wiki/Reverse_Polish_notation) string, and calculates the result from that string. The program uses stacks to store operators.

The program will ask the user for an expression. The expression can contain basic operations (addition, subtraction, multiplication, division, exponentiation). Some basic functions will also be allowed. It can also include variables, which should be defined beforehand. Otherwise the program will raise an error. The program will also check that the expression does not contain any invalid signs or characters, and that the amount of left and right parentheses matches. If the expression is valid, the program will transform it to an RPN string by using the shunting-yard algorithm. Finally, the RPN string will be used to calculate the result.

The time and space complexities should be O(n), where n is the length of the expression given. All of my documentation and code is going to be written in English.

My degree programme is bachelor's degree in computer science.

#### Sources:
* https://en.wikipedia.org/wiki/Shunting-yard_algorithm
* https://en.wikipedia.org/wiki/Reverse_Polish_notation
