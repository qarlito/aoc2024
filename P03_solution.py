from P03_input import DEMO_INPUT, DEMO_INPUT2, PRODUCTION_INPUT

import sys
if len(sys.argv) > 1 and sys.argv[1].startswith('d'):
    INPUT = DEMO_INPUT
    INPUT2 = DEMO_INPUT2
else:
    INPUT = PRODUCTION_INPUT
    INPUT2 = PRODUCTION_INPUT

import re

offset = 0
total = 0
while True:
    m = re.search('mul\\(\\d\\d?\\d?,\\d\\d?\\d?\\)', INPUT[offset:])
    if m is None:
        break
    mul = INPUT[offset + m.start() : offset + m.end()]
    offset += m.end()

    m = re.match('mul\\((\\d\\d?\\d?),(\\d\\d?\\d?)\\)', mul)
    if m is None:
        raise Exception(f'Error: cannot parse {mul}')
    total += int(m.groups()[0]) * int(m.groups()[1])
print(f'Problem 1: {total}')


offset = 0
total = 0
enabled = True
while True:
    m = re.search("(mul\\(\\d\\d?\\d?,\\d\\d?\\d?\\)|do\\(\\)|don't\\(\\))", INPUT2[offset:])
    if m is None:
        break
    offset += m.end()
    print(f'Found {m.group()}')
    if m.group() == 'do()':
        enabled = True
    elif m.group() == "don't()":
        enabled = False
    else:
        mul = m.group()
        m = re.match('mul\\((\\d\\d?\\d?),(\\d\\d?\\d?)\\)', mul)
        if m is None:
            raise Exception(f'Error: cannot parse {mul}')
        if enabled:
            total += int(m.groups()[0]) * int(m.groups()[1])
print(f'Problem 2: {total}')


