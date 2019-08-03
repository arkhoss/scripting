#! /usr/bin/python3
#Usage: logical-operators-and-conditionals.py 
#Author: David Caballero <d@dcaballero.net>
#Version: 1.0

# < > <= >= != ==

print(5 < 6)

print(5 > 6)

print(5 <= 6)

print(5 >= 6)

print(5 != 6)

print(5 == 5)

print( 'abc' == 'abc' )

# not and or
print("not and or")

a = True
b = False
print(not a)
print(a and b)
print(b and b)
print(a and a)
print(a or a)
print(b or b)
print(a or b)

d = 5
e = 1
f = False
g = 'python'
h = 'some'
z = not((not( e <= d) and (g >= h )) or f) and 1
