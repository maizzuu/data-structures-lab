# Testing document

## Unit tests

The unit tests were done with the unittest library. The tested files were `calculator.py`, `evaluator.py` and `shunting_yard.py`. The tests include different kinds of inputs, both valid and invalid ones. They also test that rounding answers works and that error messages work. Also all variable actions, such as storing and listing are tested. A stub IO class was created to inject inputs and check outputs.  
The tests can be run and a coverage report created by running

`poetry run invoke coverage-report`

After that the report can be found from htmlcov/index.html, or it can be opened with the command

`poetry run invoke open-report`
