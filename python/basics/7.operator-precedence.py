#! /usr/bin/python3
#Usage: operator-precedence.py 
#Author: David Caballero <d@dcaballero.net>
#Version: 1.0

print("First example")
print(25*15+33/2.0)

a = 25 * 15
b = 33 / 2.0
print(a + b)

print("Second example")
print((25 * 15 + 33)/2.0)

a = 25 * 15 + 33
b = 2.0
print(a/b)

print((5.0 * (8 + (16 - 2.0)/(4+1))/2) % 4)
a = 16 - 2.0
b = 4 +1 
c = a / b
d = 8 + c
e = d / 2 
f = 5.0 * e
g = f % 4 
print(g)
