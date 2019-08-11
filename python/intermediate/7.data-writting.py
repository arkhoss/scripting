#!/usr/bin/python3
#Usage: data-writting.py
#Author: David Caballero <d@dcaballero.net>
#Version: 1.0

f = 'write.txt'

file = open( f,"w+")
file.write("Hello file. I am string!")
file.seek(0)
print(file.read())
file.close()


file = open( f,"w+")
file.write("Hello file. I am string!")
file.seek(0)
file.write("this")
file.seek(0)
print(file.read())
file.close()
