# Week 2

This week I started writing the code for the calculator. I started with the easiest parts of the algorithm, and now only 
the parsing of expressions containing functions is missing. I have to figure out how the algorithm will read and understand the functions.
Right now the program only turns the expression from infix notation to RPN, it doesn't calculate the result.

I also wrote some basic unit tests, and my branch coverage is quite high (93%). I configured Github Actions for continuous integration and configured
pylint (8.75/10). 

I had to learn more about dependency injection to get my tests to work. 

I am not sure whether I should test the CalculatorIO class or not.

Next week I think I will separate my algorithm into a separate class or at least into multiple methods because right now the code looks horrible
and it is difficult to read. I will also start writing code for the algorithm that will calculate the result of the expression.
