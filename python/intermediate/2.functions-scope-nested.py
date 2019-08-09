#! /usr/bin/python3
#Usage: functions-scope-nested.py
#Author: David Caballero <d@dcaballero.net>
#Version: 1.0

def scope(a):
    a = a + 1
    print(a)
    return a
scope(5)
# print(a)

# Nested

def outer(a):

    def nested(b):
        return b * a;

    a = nested(a)
    return a

print(outer(4))


def f(a):
    def g(b):
        def h(c):
            return a * b * c
        return h

    return g

print(f(5)(2)(3))
