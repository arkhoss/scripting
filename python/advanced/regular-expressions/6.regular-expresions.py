#!/usr/bin/python3

import re

print(re.findall('x*y','xxxyyyxxxy'), re.IGNORECASE)

print(re.findall('(^XY{2}) | (yx{2}$)', 'xyxyxxxyxx\nxyyxxxxx'), re.MULTILINE)

print(re.findall('z.x', 'xyxyxxxyxx\nxyyxxxxx'))
print(re.findall('z.x', 'xyxyxxxyxx\nxyyxxxxx'), re.DOTALL)
