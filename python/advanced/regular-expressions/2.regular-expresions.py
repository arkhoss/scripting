#!/usr/bin/python3

import re

def all_matches(text,pattern):
    print(pattern)
    regobj = re.compile(pattern)
    for m in regobj.finditer(text):
        print(str(m.start()) + '-' + str(m.end()) + ':' + text[m.start() : m.end()])

all_matches('xyyxxxxxyyyyxxxxyy','xy*')
all_matches('xyyxxxxxyyyyxxxxyy','xy+')
all_matches('xyyxxxxxyyyyxxxxyy','xy?')


all_matches('xyyxxxxxyyyyxxxxyy','xy{3,4}')
all_matches('xyyxxxxxyyyyxxxxyy','xy+?')
all_matches('xyyxxxxxyyyyxxxxyy','xy??')

all_matches('xyyxxxxxyyyyxxxxyy','xy{3,}')

all_matches('xyyxxxxxyyyyxxxxyy','x[xy]+')

all_matches('xx.. ..yyyxxx.. ','[^. ]+')

all_matches('A94B2c4 xyz', '[A-Z][0-9]')

all_matches('A94B2c4 xyz', '[A-Za-z][0-9]')


all_matches('Silk road', 'S.+k')
all_matches('Silk road', 'r.+d')

all_matches('This is 1-st example', r'\d+')
all_matches('This is 1-st example', r'\D+')

all_matches('This is 1-st example', r'\s+')
all_matches('This is 1-st example', r'\W+')

all_matches('Relative position in regular expression', r'\w+')
all_matches('Relative position in regular expression', r'\w+$')
all_matches('Relative position in regular expression', r'\A\w+')

all_matches('Relative position in regular expression', r'\w+\Z')
