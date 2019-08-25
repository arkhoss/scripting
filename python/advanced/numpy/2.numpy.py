#!/usr/bin/python3

import numpy as np

a1 = np.array([2,1,3,4])
a2 = np.array([[1,2,1],[2,1,2],[1,2,3]])
a3 = np.array([[[1,2,1],[2,1,2]],[[2,2,3],[1,2,3]],[[3,2,3],[1,2,3]]])
a4 = np.arange(10,50,10)
a5 = np.arange(15)
a6 = np.arange(10,20)
a7 = np.arange(0.3,2,0.2)
a8 = np.linspace(3, 9, 9)
o1 = np.ones((2,2,2))
o2 = np.zeros((2,2,2))
e1 = np.empty((3,4))
e2 = np.eye(5)
r1 = np.random.random((5,5))

print(a2.shape)
print(a2.size)
print(a2.dtype)

print(a7.itemsize)
print(a7.dtype)

#print(a1.shape)
#print(a1.reshape(2,2))
#print(a1.shape)

try:
    print(a3.shape)
    print(a3.reshape(3,6))
except Exception as e:
    print(e)

a3.resize(3,2,3)
print(a3[0,:,:])
print(a3[0,...])
print(a3[0])


print(a3)
print("------------")
print(a3[1:3])
print("------------")
print(a3[1:3, 0, 1:3])


c1 = np.arange(15)
b1 = c1 > 9
print(c1)
print(b1)

c2 = np.arange(25).reshape(5,5)

print(c2)
print(c2.max())
print(c2.min())
print(c2.sum())
print(c2.cumsum())
print(c2.max(axis=0))
print(c2.max(axis=1))
print(c2.min(axis=0))
print(c2.min(axis=1))

print(c2.cumsum(axis=0))
print(c2.cumsum(axis=1))


c3 = c2.copy()

c3[0,0] = 16

print(c2 is c3)
print(c2)
print(c3)
