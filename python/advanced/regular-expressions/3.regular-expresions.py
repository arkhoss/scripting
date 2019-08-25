#!/usr/bin/python3

import re

regex = re.compile('x([xy]+)(y)')
match = regex.search('xyxxxyxxxyxyxy')
print(match.group(0))
print(match.group(1))
print(match.group(2))

print(match.group(2))


regex = re.compile('x(?P<first>[xy]+)(?<second>y)')
match = regex.search('xyxxxyxxxyxyxy')
print(match.groups())
print(match.groups('second'))
