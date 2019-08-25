#!/usr/bin/python3

import numpy as np

v1 = np.array([2,1,3,4])
v2 = np.array([5,1,7,6])

print(np.vstack((v1,v2)))
print(np.hstack((v1,v2)))


x = np.arange(9).reshape(3,3)
y = np.arange(10,19).reshape(3,3)

print(x > 4)

print(x < 4)

print(x == 4)

print(x)
print(y)

print(x*y)

a = np.array([[1,1],[2,2],[3,3]])
b = np.array([[1,2,3,4,5],[1,2,3,4,5]])

print(a)
print(b)

print(np.dot(a, b))
