#! /usr/bin/python3
#Usage: basic-strings-manipulation.py 
#Author: David Caballero <d@dcaballero.net>
#Version: 1.0

string = 'I am string in Python'
string1 = "I am a string in Python"

string[0]
# string[-1] = 'x'

len('My length is 15')

len(string)

print(string[-2])

print(string[5:11])

print(string[:5])

string2 = 2 * ( 'Con' + 'catenation' )

print(string2)

con = 'con'
cat = 'catenate'

print( con + cat )
 
print( con + 'catenate' )

word = "Ford"
word = 'L' + word[1:]

print(word)
