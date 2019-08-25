#!/usr/bin/python3
#Usage: lambda.py
#Author: David Caballero <d@dcaballero.net>
#Version: 1.0

print("------------------- modules -----------------------")
import prime

prime.PrimeTo(10)

import prime as pr

pr.PrimeTo(10)

from prime import PrimeTo

PrimeTo(10)

import prime
print(dir(prime))

print("------------------- packages -----------------------")
___init__
