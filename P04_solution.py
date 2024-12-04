from P04_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT

import sys
if len(sys.argv) > 1 and sys.argv[1].startswith('d'):
    INPUT1 = DEMO_INPUT1.strip()
    INPUT2 = DEMO_INPUT2.strip()
else:
    INPUT1 = PRODUCTION_INPUT.strip()
    INPUT2 = INPUT1


# Part 1

data = INPUT1.splitlines()   # Acts like a matrix
assert len(data) == len(data[0])
size = len(data)

hor = [row for row in data]
ver = list()
for colnum in range(size):
    ver.append(''.join([row[colnum] for row in data]))
diag1 = list()
for i in range(size-1, 0, -1):
    diag1.append(''.join([data[i+j][j] for j in range(size-i)]))
for i in range(0, size):
    diag1.append(''.join([data[j][i+j] for j in range(size-i)]))
diag2 = list()
for i in range(size-1, 0, -1):
    diag2.append(''.join([data[i+j][size-1-j] for j in range(size-i)]))
for i in range(0, size):
    diag2.append(''.join([data[j][size-1-(i+j)] for j in range(size-i)]))
#print(hor)
#print(ver)
#print(diag1)
#print(diag2)

domain = ['-'.join(hor), '-'.join(ver), '-'.join(diag1), '-'.join(diag2)]

alldomain = '|'.join(domain)

#print(alldomain)
xmas_count = alldomain.count('XMAS')
samx_count = alldomain.count('SAMX')
print(xmas_count, samx_count, xmas_count+samx_count)



# Part 2

data = INPUT2.splitlines()   # Acts like a matrix
assert len(data) == len(data[0])
size = len(data)

count = 0
for x in range(size-2):
    for y in range(size-2):
        if {data[x][y], data[x+2][y+2]} == {'M','S'} and data[x+1][y+1]=='A' and {data[x+2][y], data[x][y+2]} == {'M','S'}:
            count += 1
print(count)
