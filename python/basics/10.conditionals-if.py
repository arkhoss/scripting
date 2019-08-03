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

if 5 < 7:
    if 5 > 6:
        print("5 > 6")
    else:
        print('5 <= 6')
