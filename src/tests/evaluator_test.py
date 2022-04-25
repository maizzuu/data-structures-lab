import unittest
from evaluator import Evaluator


class TestEvaluator(unittest.TestCase):
    def setUp(self):
        self.eval = Evaluator("")

    def test_single_number(self):
        self.eval.set_expression("3")

        result = self.eval.evaluate()

        self.assertEqual(result, 3)

    def test_basic_operations(self):
        self.eval.set_expression("2 2 * 4 2 / - 3 +")

        result = self.eval.evaluate()

        self.assertEqual(result, 5.0)

    def test_power(self):
        self.eval.set_expression("3 2 ^")

        result = self.eval.evaluate()

        self.assertEqual(result, 9)

    def test_float(self):
        self.eval.set_expression("2.5 3 +")

        result = self.eval.evaluate()

        self.assertEqual(result, 5.5)

    def test_abs(self):
        self.eval.set_expression("-3 abs 4 +")

        result = self.eval.evaluate()

        self.assertEqual(result, 7.0)

    def test_cos(self):
        self.eval.set_expression("0 cos 2 +")

        result = self.eval.evaluate()

        self.assertEqual(result, 3.0)

    def test_exp(self):
        self.eval.set_expression("3 exp 4 *")

        result = self.eval.evaluate()

        self.assertEqual(result, 80.342)

    def test_logs(self):
        self.eval.set_expression("2 lb 5 lg + 4 ln -")

        result = self.eval.evaluate()

        self.assertEqual(result, 0.313)

    def test_sin(self):
        self.eval.set_expression("8 sin 2 /")

        result = self.eval.evaluate()

        self.assertEqual(result, 0.495)

    def test_sqrt(self):
        self.eval.set_expression("36 sqrt 5 -")

        result = self.eval.evaluate()

        self.assertEqual(result, 1)

    def test_tan(self):
        self.eval.set_expression("3 tan 6 -")

        result = self.eval.evaluate()

        self.assertEqual(result, -6.143)
