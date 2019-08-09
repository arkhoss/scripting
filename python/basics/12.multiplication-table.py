#! /usr/bin/python3
#Usage: multiplication-table.py
#Author: David Caballero <d@dcaballero.net>
#Version: 1.0


for i in range(1,11):
    print('{:<3}|'.format(i),end="")

    for j in range(1,11):
        print('{:>4}|'.format(i * j),end="")

    print('\n')
