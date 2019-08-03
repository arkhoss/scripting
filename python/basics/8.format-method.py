#! /usr/bin/python3
#Usage: format-method.py 
#Author: David Caballero <d@dcaballero.net>
#Version: 1.0

print("Today I  had {0} cups of {1}".format(3, "coffee"))
print('prices: ({x}, {y}, {z})'.format(x = 2.0, y = 1.5, z = 5))
print("The {vehicle} had {0} crashes i {1} months".format(5,6, vehicle = 'car'))

# {:character>}.format("string")
print('{:<20}'.format("text"))
print('{:>20}'.format("text"))

# binary
print('{:b}'.format(21))
# normal
print('{:x}'.format(21))
# octal
print('{:o}'.format(21))

print('I\'m a string in "python"')

print(r'c:\number\nan')

print("""\
    Hello:
            User defined look
            Python Output""")
