#!/usr/bin/python3
#Usage: lambda.py
#Author: David Caballero <d@dcaballero.net>
#Version: 1.0


#OOP


class Complex:
    'this class simulate complex numbers'
    def __init__(self,real = 0,imag = 0):
        if(type(real) not in (int, float)) or type(imag) not in (int,float):
            raise Exception('Args are no numbers!')
        self.real = real
        self.imag = imag

try:
    c = Complex(2)
    print(c.real, c.imag)
except Exception as e:
    print(e)


try:
    c = Complex((1,2,3),[1,2,3])
    print(c.real, c.imag)
except Exception as e:
    print(e)



try:
    c = Complex(2,4)
    print(c.real, c.imag)
except Exception as e:
    print(e)
