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
        #self.__real = real
        #self.__imag = imag
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


try:
    c = Complex()
    c.SetReal((1,2,3))
    c.SetImag(1)
    print(c.GetReal(), c.GetImag())
except Exception as e:
    print(e)

try:
    c = Complex()
    # c.__real
except Exception as e:
    print(e)

try:
    c = Complex(-3,4)
    print(c.GetModulus(), c.GetPhi())
except Exception as e:
    print(e)
