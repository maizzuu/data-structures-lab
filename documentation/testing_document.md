# Testing document

## Unit tests

The unit tests were done with the unittest library. The tested files are `calculator.py`, `evaluator.py` and `shunting_yard.py`. The tests include different kinds of inputs, both valid and invalid ones. They also test that rounding answers works and that correct errors are raised. Also all variable actions, such as storing and listing are tested. A stub IO class is used for testing `calculator.py`.  
The tests can be run and a coverage report created by running

`poetry run invoke coverage-report`

### Coverage report

After running the tests, the report can be found in htmlcov/index.html, or it can be opened with the command

`poetry run invoke open-report`

Currently (27.4.) the test coverage is 100% accoring to the coverage report, but for some reason codecov says it's only 98%
