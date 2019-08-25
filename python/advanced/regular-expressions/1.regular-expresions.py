#!/usr/bin/python3

import re

# print(re.search('none','serching pattern in text'))

# match = re.search('pattern','Searching pattern in text')
print(match)

print(match.re.pattern)
print(match.string)
print(match.start())
print(match.end())


regex = re.compile('pattern')
print(regex.search('Searching pattern in text...').start())
print(regex.findall('Searching pattern in text...'))

print(re.match("Match","Match function test"))
print(re.match("Test","Match function test"))
