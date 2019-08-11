#!/usr/bin/python3
#Usage: data-input.py
#Author: David Caballero <d@dcaballero.net>
#Version: 1.0

age = input("How old are you: ")
print(age)


#open(filename, access, buffering)
file = open("/home/iopervert/tmp/file.txt","r")
print(file.read())
file.close()


#open(filename, access, buffering)
file = open("/home/iopervert/tmp/file.txt","r")
print(file.read(4))
file.close()

#open(filename, access, buffering)
file = open("/home/iopervert/tmp/file.txt","r")
print(file.read(5))
print(file.tell())
file.close()


#open(filename, access, buffering)
file = open("/home/iopervert/tmp/file.txt","r")
print(file.read(4))
file.seek(5)
print(file.tell())
file.close()


#open(filename, access, buffering)
file = open("/home/iopervert/tmp/file.txt","r")
for line in file:
    print(line)

file.close()

#open(filename, access, buffering)
file = open("/home/iopervert/tmp/file.txt","r")
print("File Name: " + file.name)
print("is closed: " + str(file.closed))
print("Mode " + file.mode)
file.close()
