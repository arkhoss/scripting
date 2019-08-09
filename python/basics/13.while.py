#! /usr/bin/python3
#Usage: multiplication-table.py
#Author: David Caballero <d@dcaballero.net>
#Version: 1.0


condition = 10

while condition != 0:
    print(condition)
    condition = condition - 1

# infinite loop
# while True:
#    print("Infinite")
#    break
#


for i in range(1,11):
    if i == 5 or i == 8:
        continue
    print(i)
