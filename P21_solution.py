#!./venv/bin/python3

from P21_input import PRODUCTION_INPUT

import math

MOVES = ['A<', 'A>', 'A^', 'Av',
         '<A', '<^', '<v',
         '>A', '>^', '>v',
         '^<', '^>', '^A',
         'v<', 'v>', 'vA']

DIRPAD = {           '^':(0,1), 'A':(0,2),
          '<':(1,0), 'v':(1,1), '>':(1,2)}

def DIRPAD_FORCED_DIRECTIONS(row1, col1, row2, col2):
    if row1==0 and col2==0:
        return ['v<']
    if col1==0 and row2==0:
        return ['>^']
    return None

NUMPAD = {'7':(0,0), '8':(0,1), '9':(0,2),
          '4':(1,0), '5':(1,1), '6':(1,2),
          '1':(2,0), '2':(2,1), '3':(2,2),
                     '0':(3,1), 'A':(3,2)}

def NUMPAD_FORCED_DIRECTIONS(row1, col1, row2, col2):
    if row1==3 and col2==0:
        return ['^<']
    if col1==0 and row2==3:
        return ['>v']
    return None

# To speed up, we could memoize this function
def best_local_path(pad, forced_directions, key1, key2):
    if key1 == key2:
        return 0, []
    row1, col1 = pad[key1]
    row2, col2 = pad[key2]
    directions = forced_directions(row1, col1, row2, col2)
    if directions is None:
        if col1==col2:
            directions = [ 'v' if row2>row1 else '^' ]
        elif row1==row2:
            directions = [ '>' if col2>col1 else '<' ]
        else:
            hdir = '>' if col2>col1 else '<'
            vdir = 'v' if row2>row1 else '^'
            directions = [hdir+vdir, vdir+hdir]
    return abs(row2-row1)+abs(col2-col1), directions

# Get cost to do a move on a pad
def get_cost(pad, pad_forced_directions, cost_of_previous_level, from_key, to_key):
    numpresses, paths = best_local_path(pad, pad_forced_directions, from_key, to_key)
    if len(paths) == 0:
        best_path_cost = 0
    else:
        best_path_cost = math.inf
        for path in paths:
            path_cost = 0
            full_path = 'A' + path + 'A'
            for i in range(len(full_path)-1):
                path_cost += cost_of_previous_level[full_path[i:i+2]]
            best_path_cost = min(best_path_cost, path_cost)
    return best_path_cost + numpresses

def get_dirpad_cost(num_levels):
    prev_cost = dict.fromkeys(MOVES, 0)  # Human operator - can move hand between buttons at zero cost
    # For each level, calculate the cost of all MOVES, given the cost of the moves at the previous level
    for level in range(num_levels):
        new_cost = dict()
        for move in MOVES:
            new_cost[move] = get_cost(DIRPAD, DIRPAD_FORCED_DIRECTIONS, prev_cost, move[0], move[1])
        prev_cost = new_cost
    return prev_cost

def get_cost_on_numpad(code, dp_cost):
    code_cost = 0
    for from_key, to_key in zip('A'+code, code):
        # Move robot from from_key to to_key
        code_cost += get_cost(NUMPAD, NUMPAD_FORCED_DIRECTIONS, dp_cost, from_key, to_key)
        # Press button
        code_cost += 1
    return code_cost

num_levels = 2
dp_cost = get_dirpad_cost(num_levels)
code = '029A'
code_cost = get_cost_on_numpad(code, dp_cost)
print(f'Example code {code} at {num_levels} levels costs {code_cost}\n')

for part, num_levels in enumerate([2, 25]):
    dp_cost = get_dirpad_cost(num_levels)
    sum_of_complexities = 0
    for code in PRODUCTION_INPUT.strip().splitlines():
        code_cost = get_cost_on_numpad(code, dp_cost)
        print(f'Code {code} at {num_levels} levels costs {code_cost}')
        assert code[3] == 'A'
        sum_of_complexities += code_cost * int(code[:3])
    print(f'Part {part+1} sum of complexities: {sum_of_complexities}\n')

