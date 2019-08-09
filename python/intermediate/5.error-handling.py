#!/usr/bin/python3
#Usage: error-handling.py
#Author: David Caballero <d@dcaballero.net>
#Version: 1.0

# division by 0 error
# print(5/0)

# file not found
# file = open("file","r")

# data type error int / string
# int('1.2b')

# int('1.2')

# division by 0 error
# a = 5/0
# print("after error")


try:
    a = 5/0
except Exception as e:
    print(e)

try:
    n = int(input("Enter an Integer: "))
except ValueError:
    print("That is not an integer")


try:
    sum = 0
    file = open('number.txt','r')
    for number in file:
        sum = sum + 1.0/int(number)
    print(sum)
except ZeroDivisionError:
    print("Number in file equal to zero!")
except IOError:
    print("File not exist")
finally:
    print(sum)
    file.close()
