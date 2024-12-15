#!/usr/local/bin/python
from P15_input import DEMO_INPUT1, DEMO_INPUT2, DEMO_INPUT3, PRODUCTION_INPUT
#from Pxx_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT

import sys
if len(sys.argv) > 1 and sys.argv[1].startswith('d'):
    INPUT1 = DEMO_INPUT1.strip()
    INPUT2 = DEMO_INPUT2.strip()
    DEMO = True
else:
    INPUT1 = PRODUCTION_INPUT.strip()
    INPUT2 = INPUT1
    DEMO = False

INPUT = INPUT1

def debug(s, new_line_before=False, new_line_after=False):
    if DEBUG:
        if new_line_before:
            print()
        print(s)
        if new_line_after:
            print()

DEBUG = DEMO


state = list()
robot_position = None
PATH = ''
part = 1
for rownum, line in enumerate(INPUT.splitlines()):
    if line == '':
        assert part == 1
        part = 2
        continue
    if part == 1:
        assert line[0] == '#'
        assert line[-1] == '#'
        state.append([c for c in line])
        if '@' in line:
            assert robot_position is None
            robot_position = (rownum, line.index('@'))
    else:
        PATH += line

NUMROWS = len(state)
NUMCOLS = len(state[0])
assert state[0] == ['#'] * NUMCOLS
assert state[-1] == ['#'] * NUMCOLS
assert robot_position is not None

MOVE_DIRECTION = {'>':(0,1), '<':(0,-1), '^':(-1,0), 'v':(1,0)}

# Coordinates are always rownum, colnum
for move in PATH:
    direction = MOVE_DIRECTION[move]
    i = 0
    while True:
        i += 1
        next_position = (robot_position[0] + i*direction[0], robot_position[1] + i*direction[1])
        element = state[next_position[0]][next_position[1]]
        if element == '.':
            # We can move/push
            state[next_position[0]][next_position[1]] = 'O'
            state[robot_position[0]][robot_position[1]] = '.'
            new_robot_position = (robot_position[0]+direction[0], robot_position[1]+direction[1])
            state[new_robot_position[0]][new_robot_position[1]] = '@'
            robot_position = new_robot_position
            break
        elif element == '#':
            # Cannot move
            break
        elif element == 'O':
            # Look further
            pass
        else:
            raise Exception(f'Unexpected element {element}')

    if DEBUG:
        print()
        print(f'Move {move}:')
        for row in state:
            print(''.join(row))

score = 0
for rownum, row in enumerate(state):
    for colnum, c in enumerate(row):
        if c == 'O':
            score += 100*rownum + colnum
print(f'Part 1 - score {score}')


#INPUT = DEMO_INPUT3.strip()

state = list()
robot_position = None
PATH = ''
part = 1
for rownum, line in enumerate(INPUT.splitlines()):
    if line == '':
        assert part == 1
        part = 2
        continue
    if part == 1:
        assert line[0] == '#'
        assert line[-1] == '#'
        row = list()
        state.append(row)
        for c in line:
            if c == '#':
                row.extend(['#', '#'])
            elif c == '.':
                row.extend(['.', '.'])
            elif c == 'O':
                row.extend(['[', ']'])
            elif c == '@':
                row.extend(['@', '.'])
                assert robot_position is None
                robot_position = (rownum, line.index('@')*2)
    else:
        PATH += line

NUMROWS = len(state)
NUMCOLS = len(state[0])
assert state[0] == ['#'] * NUMCOLS
assert state[-1] == ['#'] * NUMCOLS
assert robot_position is not None

if DEBUG:
    for row in state:
        debug(''.join(row))

# Coordinates are always rownum, colnum
for move in PATH:
    debug(f'\nMove: {move}')
    direction = MOVE_DIRECTION[move]
    if direction[0] == 0:
        # Horizontal move
        i = -1   # Try i = 1, 3, 5, ...
        while True:
            i += 2
            next_position = (robot_position[0] + i*direction[0], robot_position[1] + i*direction[1])
            element = state[next_position[0]][next_position[1]]
            if element == '.':
                for j in range((i-1)//2):
                    if direction[1] == 1:
                        # Move to the right
                        left_col = robot_position[1] + (j*2+2) * direction[1]
                    else:
                        # Move to the left
                        left_col = robot_position[1] + (j*2+3) * direction[1]
                    state[robot_position[0]][left_col] = '['
                    state[robot_position[0]][left_col+1] = ']'
                state[robot_position[0]][robot_position[1]] = '.'
                new_robot_position = (robot_position[0], robot_position[1] + direction[1])
                state[new_robot_position[0]][new_robot_position[1]] = '@'
                robot_position = new_robot_position
                break
            elif element == '#':
                # Cannot move
                break
            elif element in ('[', ']'):
                # Look further
                pass
            else:
                raise Exception(f'Unexpected element {element}')
    else:
        # Vertical move
        push_layers = [ set([robot_position[1]]) ]   # For each layer: list of positions to push
        while True:
            debug('  Starting layer')
            next_layernum = len(push_layers)
            next_layer = set()
            stuck = False
            for colnum in push_layers[-1]:
                element = state[robot_position[0] + next_layernum*direction[0]][colnum]
                debug(f'    Found {element} in position {robot_position[0] + next_layernum*direction [0]}, {colnum}')
                if element == '#':
                    # Cannot move
                    stuck = True
                    break
                elif element == '[':
                    next_layer.add(colnum)
                    next_layer.add(colnum+1)
                elif element == ']':
                    next_layer.add(colnum-1)
                    next_layer.add(colnum)

            if stuck:
                break

            if len(next_layer) > 0:
                debug(f'    Append {next_layer}')
                push_layers.append(next_layer)
            else:
                debug('    I can push', True)
                debug(f'    {push_layers}')
                for i in range(len(push_layers)-1, -1, -1):
                    push_layer = push_layers[i]
                    for j, colnum in enumerate(sorted(push_layer)):
                        # Add boxes to new layer
                        element = '[' if j%2==0 else ']'
                        state[robot_position[0]+(i+1)*direction[0]][colnum] = element
                        # Remove items from old layer
                        state[robot_position[0]+i*direction[0]][colnum] = '.'
                new_robot_position = (robot_position[0]+direction[0], robot_position[1])
                state[new_robot_position[0]][new_robot_position[1]] = '@'
                robot_position = new_robot_position
                break

    if DEBUG:
        for row in state:
            print(''.join(row)) 


total = 0
for rownum, row in enumerate(state):
    for colnum, c in enumerate(row):
        if c == '[':
            total += 100*rownum + colnum
print(f'Part 2 - total {total}')
