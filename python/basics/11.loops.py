#! /usr/bin/python3
#Usage: loops.py
#Author: David Caballero <d@dcaballero.net>
#Version: 1.0

# range(start,stop,step)


for i in range(1,10):
    print(i)


for i in range(10,20):
    print(i)


for i in range(0,13,3):
    print(i)

string = "String traversal!"
for i in range(len(string)):
    print(string[i])

string = "String traversal!"
for char in string:
    print(char)

for i in range(3):
    for j in range(2):
        print(j)
