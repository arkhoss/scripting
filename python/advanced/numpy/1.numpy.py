#!/usr/bin/python3

import numpy as np

a1 = np.array([2,1,3,4])
print(a1)

a2 = np.array([[1,2,1],[2,1,2],[1,2,3]])
print(a2)


a3 = np.array([[[1,2,1],[2,1,2]],[[2,2,3],[1,2,3]],[[3,2,3],[1,2,3]]])
print(a3)

a4 = np.arange(10,50,10)
print(a4)

a5 = np.arange(15)
print(a5)
a6 = np.arange(10,20)
print(a6)
a7 = np.arange(0.3,2,0.2)
print(a7)

a8 = np.linspace(3, 9, 9)
print(a8)

o1 = np.ones((2,2,2))
print(o1)

o2 = np.zeros((2,2,2))
print(o2)

e1 = np.empty((3,4))
print(e1)

e2 = np.eye(5)
print(e2)

r1 = np.random.random((5,5))
print(r1)
