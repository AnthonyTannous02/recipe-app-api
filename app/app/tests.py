"""
Sample Tests
"""

from app import calc
from django.test import SimpleTestCase


class CalcTests(SimpleTestCase):
    """
    Test the calc module.
    """

    def test_add_numbers(self):
        a = 1
        b = 4
        expected_res = 5

        res = calc.add(a, b)

        self.assertEqual(expected_res, res)

    def test_subtract_numbers(self):
        a = 3
        b = 2
        expected_res = 1

        res = calc.subtract(a, b)

        self.assertEquals(expected_res, res)
