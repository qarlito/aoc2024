from P05_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT

import sys
if len(sys.argv) > 1 and sys.argv[1].startswith('d'):
    INPUT1 = DEMO_INPUT1.strip()
    INPUT2 = DEMO_INPUT2.strip()
else:
    INPUT1 = PRODUCTION_INPUT.strip()
    INPUT2 = INPUT1


# Part 1

from collections import defaultdict
rules = defaultdict(lambda: set())
pagelists = list()

input_part = 1
for line in INPUT1.splitlines():
    if line == '':
        assert input_part==1
        input_part = 2
        continue
    if input_part == 1:
        astr, bstr = line.split('|')
        rules[astr].add(bstr)
    else:
        pagelists.append(line.split(','))

#print(rules)
#print('---')
#print(pagelists)

from functools import cmp_to_key

middle_sum = 0
middle_sum_corrected_pages = 0
for pagelist in pagelists:
    pagelist_sorted = sorted(pagelist, key=cmp_to_key(lambda a,b: -1 if b in rules[a] else 1))
    l = len(pagelist)
    assert l % 2 == 1 
    if pagelist == pagelist_sorted:
        middle_sum += int(pagelist[(l-1)//2])
    else:
        middle_sum_corrected_pages += int(pagelist_sorted[(l-1)//2])

print(f'Part 1 - Good pages middle sum: {middle_sum}')
print(f'Part 2 - Corrected bad pages middle sum: {middle_sum_corrected_pages}')
