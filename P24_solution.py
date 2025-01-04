#!./venv/bin/python3
from P24_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT
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


def debug(s, new_line_before=False, new_line_after=False):
    if DEBUG:
        if new_line_before:
            print()
        print(s)
        if new_line_after:
            print()

DEBUG = DEMO
INPUT = INPUT1

from collections import defaultdict

def op_and(a, b):
    return a and b

def op_or(a, b):
    return a or b

def op_xor(a, b):
    return a ^ b

OPERATORS={'AND': op_and, 'OR': op_or, 'XOR': op_xor}

known_states = dict()   # node to value          e.g. "x00" -> True
dependencies = dict()   # node to creation rule  e.g. "z00" -> {"op":"AND", "inputs":{"x00", "y00"}, "needed": {"x00", "y00"}}
enablers = defaultdict(lambda:set())       # node to set of outputs e.g. "x00" -> {"z00"}

input_part = 1
for line in INPUT.splitlines():
    if line == '':
        assert input_part == 1
        input_part = 2
        continue
    if input_part == 1:
        # First part of input
        node, value = line.split(': ')
        known_states[node] = True if value=='1' else False
    else:
        # Second part of input
        formula, output = line.split(' -> ')
        in1, op, in2 = formula.split(' ')
        dependencies[output] = {"op":OPERATORS[op], "inputs":{in1:None, in2:None}}
        enablers[in1].add(output)
        enablers[in2].add(output)

debug(known_states)
debug(dependencies)
debug(enablers)

assert set(known_states).isdisjoint(set(dependencies))

final_value = 0
# Now feed the known_states into the system
while len(known_states) > 0:
    node, node_state = known_states.popitem()
    if node.startswith('z') and node_state:
        final_value |= 1 << int(node[1:])
    # Feed it
    for output in enablers.get(node, []):
        dependencies[output]["inputs"][node] = node_state
        if None not in dependencies[output]["inputs"].values():
            output_state = dependencies[output]["op"](*(dependencies[output]["inputs"].values()))
            known_states[output] = output_state

print(f'Part 1: {final_value}')


