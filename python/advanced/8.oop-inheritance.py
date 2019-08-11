#!/usr/bin/python3
#Usage: lambda.py
#Author: David Caballero <d@dcaballero.net>
#Version: 1.0

#OOP

import math

class Complex:
    'this class simulate complex numbers'
    def __init__(self,real = 0,imag = 0):
        if(type(real) not in (int, float)) or type(imag) not in (int,float):
            raise Exception('Args are no numbers!')
        self.SetReal(real)
        self.SetImag(imag)

    def GetReal(self):
        return self.__real

    def GetImag(self):
        return self.__imag

    def GetModulus(self):
        return math.sqrt(self.GetReal() * self.GetReal() + self.GetImag() * self.GetImag() )

    def GetPhi(self):
        return math.atan2(self.GetImag(), self.GetReal())

    def SetReal(self,val):
        if type(val) not in (int, float):
            raise Exception('real part must be a number')
        self.__real = val

    def SetImag(self,val):
        if type(val) not in (int, float):
            raise Exception('imag part must be a number')
        self.__imag = val

    def __str__(self):
        return str(self.GetReal()) + '+' + str(self.GetImag()) + 'i';

    def __add__(self, other):
        return Complex(self.GetReal() + other.GetReal(), self.GetImag() + other.GetImag())

    def __mul__(self, other):
        if type(other) in (int, float):
            return Complex(self.GetReal() * other, self.GetImag() *  other)
        else:
            return Complex(self.GetReal() * other.GetReal() - self.GetImag() * other.GetImag(),
            self.GetImag() * other.GetImag() + self.GetReal() * other.GetReal())

    def __truediv__(self, other):
        if type(other) in (int, float):
            return Complex(self.GetReal() / float(other), self.GetImag() / float(other))
        else:
            a, b, c, d = self.GetReal(), self.GetImag(), other.GetReal(), other.GetImag()
            nominator = c * c + d * d
            return Complex(((a * c + b * d ) / nominator), ((b*c - a*d)/nominator))


try:
    a = Complex(5, 0.3)
    b = Complex(-3, 4)
    print(a + b)
except Exception as e:
    print(e)


try:
    a = Complex(5, 0.3)
    b = Complex(-3, 4)
    print(a * 2)
except Exception as e:
    print(e)

try:
    a = Complex(5, 0.3)
    b = Complex(-3, 4)
    print(a / b)
    print(a / 2)
    print(b / 2)
except Exception as e:
    print(e)
