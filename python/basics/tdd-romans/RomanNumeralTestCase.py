#!/usr/bin/python3

import unittest

# from roman_numeral_generator import RomanNumeralGenerator
from RomanNumeralGenerator import RomanNumeralGenerator


class RomanNumeralTestCase(unittest.TestCase):

    maxDiff = None

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.testclass = RomanNumeralGenerator()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_one(self):
        # Does 1 return I?
        result = self.testclass.generator(1)
        self.assertEqual('I', result, "It doesn't return I")

    def test_two(self):
        result = self.testclass.generator(2)
        self.assertEqual('II', result, "It doesn't return II")

    def test_four(self):
        result = self.testclass.generator(4)
        self.assertEqual('IV', result, "It doesn't return IV")

    def test_sixty(self):
        result = self.testclass.generator(65)
        self.assertEqual('LXV', result, "It doesn't return LXV")

    def test_max(self):
        result = self.testclass.generator(1066)
        self.assertEqual('MLXVI', result, "It doesn't return MLXVI")

if __name__ == '__main__':
    unittest.main()
