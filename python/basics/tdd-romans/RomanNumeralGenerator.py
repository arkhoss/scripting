#!/usr/bin/python3

class RomanNumeralGenerator(object):

    def generator(self, arabic):
        roman = self.to_roman(arabic)
        return roman

    def to_roman(self, number):
        roman_number = ""
        arabic_remainder = number

        if (arabic_remainder >= 1000):
            roman_number += 'M'
            arabic_remainder -= 1000

        if (arabic_remainder >= 500):
            roman_number += 'D'
            arabic_remainder -= 500

        if (arabic_remainder >= 100):
            roman_number += 'C'
            arabic_remainder -= 100

        if (arabic_remainder == 40):
            roman_number += 'XL'
            arabic_remainder -= 40

        if (arabic_remainder >= 50):
            roman_number += 'L'
            arabic_remainder -= 50

        if (arabic_remainder == 9):
            roman_number = 'IX'
            arabic_remainder -= 9

        if (arabic_remainder >= 10):
            roman_number += 'X'
            arabic_remainder -= 10

        if (arabic_remainder == 4):
            roman_number = 'IV'
            arabic_remainder -= 4

        if (arabic_remainder >= 5):
            roman_number += 'V'
            arabic_remainder -= 5

        while (arabic_remainder > 0):
            roman_number += 'I'
            arabic_remainder -= 1

        return roman_number
