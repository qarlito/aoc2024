#!/usr/local/bin/python
from P11_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT
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


def debug(s, new_line_before=False, new_line_after=False):
    if DEBUG:
        if new_line_before:
            print()
        print(s)
        if new_line_after:
            print()


INPUT = INPUT1

def create_stone(stone_str):
    stone_value = int(stone_str)
    stone_str = str(stone_value)   # To deal with inputs such as '000422'
    stone_can_split = len(stone_str) % 2 == 0
    return (stone_str, stone_value, stone_can_split)


stones = [create_stone(stone_str) for stone_str in INPUT.split(' ')]

MAX_ITERATIONS = 25
for i in range(MAX_ITERATIONS):
    new_stones = list()
    for stone_str, stone_value, stone_can_split in stones:
        if stone_value == 0:
            new_stones.append(create_stone('1'))
        elif stone_can_split:
            stone_size = len(stone_str)
            assert stone_size % 2 == 0
            new_stones.append(create_stone(stone_str[:stone_size//2]))
            new_stones.append(create_stone(stone_str[stone_size//2:]))
        else:
            new_stone_value = stone_value * 2024
            new_stone_str = str(new_stone_value)
            new_stones.append(create_stone(new_stone_str))
    stones = new_stones
    debug(f'After {i+1} iterations I have {len(stones)} stones')
print(f'\nPart 1 -- After {MAX_ITERATIONS} iterations I have {len(stones)} stones\n')



# Seems like we only visit a relatively small number of values
# Instead lets calculate each iteration how many stones we have of which value


from collections import defaultdict
stones = defaultdict(lambda: 0)  # stone_value: stone_count
for stone_str in INPUT.split(' '):
    stones[int(stone_str)] += 1

MAX_ITERATIONS = 75
for i in range(MAX_ITERATIONS):
    new_stones = defaultdict(lambda: 0)

    for stone_value, stone_count in stones.items():
        if stone_value == 0:
            new_stones[1] += stone_count
        else:
            stone_str = str(stone_value)
            stone_size = len(stone_str)
            if stone_size % 2 == 0:
                left_stone_value = int(stone_str[:stone_size//2])
                new_stones[left_stone_value] += stone_count
                right_stone_value = int(stone_str[stone_size//2:])
                new_stones[right_stone_value] += stone_count
            else:
                new_stones[stone_value * 2024] += stone_count

    stones = new_stones

print(f'\nPart 2 -- After {MAX_ITERATIONS} iterations I have {sum(stones.values())} stones.\n')
