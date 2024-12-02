from P01_input import DEMO_INPUT, PRODUCTION_INPUT

import sys
if len(sys.argv) > 1 and sys.argv[1].startswith('d'):
    INPUT = DEMO_INPUT
else:
    INPUT = PRODUCTION_INPUT



lefts, rights = zip(*[line.split('   ') for line in INPUT.strip().splitlines()])

left = sorted(map(int, lefts))
right = sorted(map(int, rights))
#print(left)
#print(right)


print('\npart 1')
print(sum((abs(l-r) for (l,r) in zip(left,right))))


similarity = 0
for l in left:
    similarity += right.count(l) * l
print('\npart 2')
print(similarity)
