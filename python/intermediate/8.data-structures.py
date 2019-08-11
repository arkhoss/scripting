#!/usr/bin/python3
#Usage: data-structures.py
#Author: David Caballero <d@dcaballero.net>
#Version: 1.0

print("------------------- tuple -----------------------")
tup = (1, 'abc', 2, 'cde')
tup1 = 3, 'efg', True

tup2 = 'A' #
print(tup[0:2])


try:
    tup[3] = 5
except Exception as e:
    print(e)


tup = tup[0:3] + (5,)
print(tup)
print(tup2 * 4)
print(5 in tup)
for x in ('a','b','c'):
    print(x)
def multiple_result():
    return(1,2,'a')
print(multiple_result())
print((1,2,3) == (1,2))

print("------------------- tuple functions -----------------------")
tup = (2,3,4)
print(max(tup))


print("------------------- list -----------------------")

list1 = [1, 'abc', (2,3)]
print(list1[2][0])


print(list1 * 2)
print('abc' in list1)
print(2 in list1)
print(list1 == [1, 'abc', (2,3)])
print(list1[:2])


list1.append(6)
list1[len(list1):] = [7]
print(list1)

print("------------------- list functions -----------------------")

print(list(map(lambda x: x**2 + 3*x + 1, [1,2,3,4])))


print(list(filter(lambda x: x < 4, [1,2,3,4,5,4,3,2,1])))

import functools

print(functools.reduce(lambda x, y: x * y, [1,2,3,4]))



print("------------------- Dictionaries -----------------------")

my_dictionary = {'Key': 'Value', ('K','E','Y'):5}
my_dictionary1 = { x: x + 1 for x in range(10) }

print(my_dictionary['Key'])
print(my_dictionary1)


try:
    print(my_dictionary[1])
except Exception as e:
    print(e)


print(my_dictionary.keys())
print(my_dictionary.values())

my_dictionary[1] = 3
print(my_dictionary)

del my_dictionary[1]
print(my_dictionary)

my_dictionary.clear()
print(my_dictionary)



print("------------------- Shallow copies -----------------------")

my_dictionary = {'Item': 'Shirt', 'Size': 'Medium', 'Price': 50}

my_dictionary1 = my_dictionary

print(my_dictionary)
my_dictionary['Size'] = 'Small'
print(my_dictionary)
print(my_dictionary1)

print("------------------- Sets -----------------------")


my_set = set(['one','two','three','one'])
my_set1 = set(['two','three','four'])

# union
print(my_set1 | my_set)

# intersection
print(my_set1 ^ my_set)

# diff
print(my_set1 - my_set)


my_set.add('five')
print(my_set)


print(set.union(my_set, my_set1))

print(set.difference(my_set, my_set1))

print(set.intersection(my_set, my_set1))
