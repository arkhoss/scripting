#! /usr/bin/python3
#Usage: logical-operators-and-conditionals.py
#Author: David Caballero <d@dcaballero.net>
#Version: 1.0

passerby_speech = 'hello'

if passerby_speech ==  'hello' or passerby_speech == 'hi':
    print("Hi, How are you?")

if True:
    print("It is True")


if passerby_speech ==  'hello' or passerby_speech == 'hi':
    print("Hi, How are you?")
else:
    print('Hey')

if 5 > 7:
    if 5 > 6:
        print("5 > 6")
    else:
        print('5 <= 6')
else:
    print(" not true!")


passerby_speech = "Hi"

if passerby_speech ==  "hello":
    print("Hi")
elif passerby_speech == "Hi":
    print("Hello")
else:
    print("Hey")


num = 3

if(num > 1 and num < 5):
    print(num)
elif ( num > 2  and num < 4):
    print(num+1)
else:
    print(num-1)


# Tennary

passerby_speech = "Hi"
me = "Hi" if passerby_speech == "Hello" or passerby_speech == "Hi" else "hey"
print(me)


a = 3
a = 7 if 3**3 > 9 else 14
print(a)
