#! /usr/bin/python3
#Usage: functions.py
#Author: David Caballero <d@dcaballero.net>
#Version: 1.0

def function():
    print("This is our first function")

def anotherfun():
    print("This is our another function")


anotherfun()
function()


def returning():
    return "I am a result!"

result = returning()

print(result)


def multival():
    return "this is a result,",2

print(multival())


def parameters(a):
    print(a)

parameters("This is a parameter")


def add(a,b):
    print(a)
    print(b)
    c = a + b
    return c

result = add(12,5)

print(result)


def add(a,b):
    print(a)
    print(b)
    c = a + b
    return c

result = add("One","word")

print(result)


def default_param(a,b = 4 ,c = 5):
    return a + b + c

result = default_param(3)

print(result)
