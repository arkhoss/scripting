#!/usr/bin/python3

import re

regex = re.compile('x(?P<first>[xy]+)(?<second>y)')
match = regex.search('xyxxxyxxxyxyxy')
print(match.groups())
print(match.group('second'))
