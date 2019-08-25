#!/usr/bin/python3

import re

regex = re.compile('y((x|y)+)')
match = regex.search('yxxyyxyxy')
print(match.group(1))
print(match.group(2))
