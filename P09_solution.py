#!/usr/local/bin/python
from P09_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT
#from Pxx_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT

import sys
if len(sys.argv) > 1 and sys.argv[1].startswith('d'):
    INPUT1 = DEMO_INPUT1.strip()
    INPUT2 = DEMO_INPUT2.strip()
    DEBUG = True
else:
    INPUT1 = PRODUCTION_INPUT.strip()
    INPUT2 = INPUT1
    DEBUG = False

INPUT = INPUT1




# Part 1
print('Starting part 1\n')

data = list()
assert len(INPUT) % 2 == 1
INPUT += '0'
for i in range(len(INPUT)//2):
    id_ = i
    num_file_bytes = int(INPUT[i*2])
    num_empty_bytes_post = int(INPUT[i*2+1])
    data += [id_] * num_file_bytes
    data += ['.'] * num_empty_bytes_post


result = data.copy()
last_left_offset = -1
while True:
    c = result.pop()
    if c == '.':
        continue
    try:
        new_left_offset = result.index('.', last_left_offset+1)
    except ValueError:
        result.append(c)
        break
    result[new_left_offset] = c
    last_left_offset = new_left_offset
    #print(''.join([str(r) for r in result]))

def checksum(result):
    result_value = 0
    for i, v in enumerate(result):
        if v != '.':
            result_value += i * v
    return result_value

print(f'\nPart 1 - result = {checksum(result)}')




# Part 2
print('\n\n\n\nStarting part 2\n')

# Data structure is two lists:
#    files = { file_id : (file_offset, file_size) }
#    gaps  = [(gap_offset, gap_size), ...]     # increasing gap_offset
# Invariant: gaps can never have size zero, and can never be adjacent to each other
# Invariant: gaps and files can never overlap
# Note that there is no invariant that every position is a gap or a file.


def display(files, gaps, line_length=50):
    if not DEBUG:
        return
    s = ['_'] * line_length
    for file_id in sorted(files.keys()):
        file_offset, file_size = files[file_id]
        for i in range(file_size):
            s[file_offset+i] = file_id
    for gap_offset, gap_size in gaps:
        for i in range(gap_size):
            s[gap_offset+i] = '.'
    print(''.join([str(c) for c in s]))


FILES = dict()
GAPS = list()
offset = 0
for i in range(len(INPUT)//2):
    file_id = i
    file_size = int(INPUT[i*2])
    assert file_size > 0
    FILES[file_id] = (offset, file_size)
    offset += file_size
    gap_size = int(INPUT[i*2+1])
    # Skip gaps of size 0 to satisfy constraint
    if gap_size != 0:
        GAPS.append((offset, gap_size))
        offset += gap_size

gaps = GAPS.copy()
files = FILES.copy()

if DEBUG:
    display(files, gaps)
    print()

for file_id in range(len(files)-1, -1, -1):
    file_offset, file_size = files[file_id]
    for gap_id, (gap_offset, gap_size) in enumerate(gaps):
        if file_offset < gap_offset:
            # Leave file where it is; cannot move to the left
            break
        elif file_size > gap_size:
            # Gap too small; try next gap
            continue
        else:
            # Move file in gap
            files[file_id] = (gap_offset, file_size)

            # For this puzzle we do not need to create a new gap where the file used to be.
            # Consider this space lost... It is not a gap nor a file.

            # Calculate new gap
            new_gap_offset = gap_offset + file_size
            new_gap_size = gap_size - file_size
            if new_gap_size == 0:
                # Remove gap
                gaps.pop(gap_id)
                break
            if gap_id < len(gaps)-1:
                next_gap_offset, next_gap_size = gaps[gap_id+1]
                if new_gap_offset + new_gap_size == next_gap_offset:
                    # Glue them together
                    gaps.pop(gap_id+1)
                    gaps[gap_id] = (new_gap_offset, new_gap_size + next_gap_size)
                    break
                else:
                    # Replace gap
                    gaps[gap_id] = (new_gap_offset, new_gap_size)
                    break
    display(files, gaps)


result_value = 0
for file_id, (file_offset, file_size) in files.items():
    for i in range(file_size):
        result_value += file_id * (file_offset + i)
print(f'\nPart 2 - result = {result_value}\n')
