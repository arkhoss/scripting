#!/usr/bin/python3
#Usage: lambda.py
#Author: David Caballero <d@dcaballero.net>
#Version: 1.0


import copy

my_dictionary = {'Key':'Value', ('K','E','Y'):5}
my_dictionary1 = copy.deepcopy(my_dictionary)

my_dictionary[1] = 1

print(my_dictionary)
print(my_dictionary1)


import math as m

print( m.cos(m.pi))
print( m.exp(m.pi))
print( m.ceil(m.pi))


import cmath as cm

print(dir(cm))

print(cm.sqrt(4))

print(cm.polar(complex(0,1)))

import random as ran

print(dir(ran))

print(ran.sample([1,2,3,4,5] ,3))

print(ran.random())

print(ran.randint(5,100))

import sys

print(sys.version)
print(sys.path)
