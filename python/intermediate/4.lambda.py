#!/usr/bin/python3
#Usage: lambda.py
#Author: David Caballero <d@dcaballero.net>
#Version: 1.0

f = lambda x, y: x + y

print(f(2,3))


f = lambda a: lambda b: lambda c: a * b * c

print(f(5)(3)(2))

f = lambda c: lambda a, b:lambda d: (c * (a + b) ) % d

print(f(2)(4,3)(11))
