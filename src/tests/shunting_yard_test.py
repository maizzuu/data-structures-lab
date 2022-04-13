import unittest
from shunting_yard import InvalidInputError, MismatchedParenthesesError, ShuntingYard, UnknownInputError


class TestShuntingYard(unittest.TestCase):
    def setUp(self):
        self.shunting_yard = ShuntingYard("", {})

    def test_plus(self):
        self.shunting_yard.expression = "1+2"

        result = self.shunting_yard.parse()

        self.assertEqual(result, "1 2 +")

    def test_minus(self):
        self.shunting_yard.expression = "1-2"

        result = self.shunting_yard.parse()

        self.assertEqual(result, "1 2 -")

    def test_decimal(self):
        self.shunting_yard.expression = "1.235+4"

        result = self.shunting_yard.parse()

        self.assertEqual(result, "1.235 4 +")

    def test_division(self):
        self.shunting_yard.expression = "2/3"

        result = self.shunting_yard.parse()

        self.assertEqual(result, "2 3 /")

    def test_parentheses(self):
        self.shunting_yard.expression = "3*(4+6)^3-(2+1)*4"

        result = self.shunting_yard.parse()

        self.assertEqual(result, "3 4 6 + 3 ^ * 2 1 + 4 * -")

    def test_short_variable(self):
        self.shunting_yard.expression = "a+3"
        self.shunting_yard.variables = {"a": "5"}

        result = self.shunting_yard.parse()

        self.assertEqual(result, "5 3 +")

    def test_invalid_input(self):
        self.shunting_yard.expression = "1,2+3"

        with self.assertRaises(InvalidInputError):
            self.shunting_yard.parse()

    def test_period_index_0(self):
        self.shunting_yard.expression = ".6+4"

        with self.assertRaises(InvalidInputError):
            self.shunting_yard.parse()

    def test_invalid_period(self):
        self.shunting_yard.expression = "6.+4"

        with self.assertRaises(InvalidInputError):
            self.shunting_yard.parse()

    def test_mismatched_parentheses(self):
        self.shunting_yard.expression = "(1+2))"

        with self.assertRaises(IndexError):
            self.shunting_yard.parse()

    def test_adjacent_operators(self):
        self.shunting_yard.expression = "2*/3"

        with self.assertRaises(InvalidInputError):
            self.shunting_yard.parse()

    def test_negative_number(self):
        self.shunting_yard.expression = "-5+(-6)"

        result = self.shunting_yard.parse()

        self.assertEqual(result, "-5 -6 +")

    def test_parentheses_left_in_opstack(self):
        self.shunting_yard.expression = "3*(4+8)("

        with self.assertRaises(MismatchedParenthesesError):
            self.shunting_yard.parse()

    def test_one_letter_variable_unknown(self):
        self.shunting_yard.expression = "2+a"

        with self.assertRaises(UnknownInputError):
            self.shunting_yard.parse()

    def test_one_letter_variable_invalid(self):
        self.shunting_yard.expression = "2a"
        self.shunting_yard.variables = {"a": "5"}

        with self.assertRaises(InvalidInputError):
            self.shunting_yard.parse()

    def test_function(self):
        self.shunting_yard.expression = "4+sqrt(9)"

        result = self.shunting_yard.parse()

        self.assertEqual(result, "4 9 sqrt +")

    def test_invalid_precedes_var(self):
        self.shunting_yard.expression = "3ab+4"

        with self.assertRaises(InvalidInputError):
            self.shunting_yard.parse()

    def test_long_var_name(self):
        self.shunting_yard.expression = "3*alpha+4"
        self.shunting_yard.variables = {"alpha": "3"}

        result = self.shunting_yard.parse()

        self.assertEqual(result, "3 3 * 4 +")

    def test_var_followed_by_invalid(self):
        self.shunting_yard.expression = "alpha3-4"
        self.shunting_yard.variables = {"alpha": "3"}

        with self.assertRaises(InvalidInputError):
            self.shunting_yard.parse()

    def test_function_missing_parentheses(self):
        self.shunting_yard.expression = "2+lb3"

        with self.assertRaises(InvalidInputError):
            self.shunting_yard.parse()

    def test_unknown_input(self):
        self.shunting_yard.expression = "sqrtt(2)"

        with self.assertRaises(UnknownInputError):
            self.shunting_yard.parse()

    def test_input_minus_and_parentheses(self):
        self.shunting_yard.expression = "-(2+1)"

        result = self.shunting_yard.parse()

        self.assertEqual(result, "0 2 1 + -")
