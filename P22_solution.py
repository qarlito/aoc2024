#!./venv/bin/python3
from P22_input import DEMO_INPUT1, DEMO_INPUT2, PRODUCTION_INPUT
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

def process(secret):
    secret = (secret ^ (secret << 6)) & 0xffffff
    secret = (secret ^ (secret >> 5))  & 0xffffff
    secret = (secret ^ (secret << 11)) & 0xffffff
    return secret

def process_n_times(secret, num_iterations):
    l = [secret]
    for i in range(num_iterations):
        secret = process(secret)
        l.append(secret)
    return l

def do_work(initial_secrets, num_iterations):
    last_digits = list()
    last_values = list()
    delta_strings = list()
    for line in initial_secrets:
        initial_secret = int(line)
        secrets = process_n_times(initial_secret, num_iterations) 
        last_digits.append([s % 10 for s in secrets[1:]])
        delta = ''.join([chr(75+(s2%10)-(s1%10)) for s1,s2 in zip(secrets, secrets[1:])])
        delta_strings.append(delta)
        last_values.append(secrets[-1])
    return last_values, delta_strings, last_digits

last_values, delta_strings, last_digits = do_work(map(int, INPUT.strip().splitlines()), 2000)
total = sum(last_values)
print(f'part 1 - {total}')


#_, delta_strings, last_digits = do_work([1, 2, 3, 2024], 2000)

global_seqdict = defaultdict(lambda:0)
for i, delta_string in enumerate(delta_strings):
    seqdict = dict()
    for j in range(len(delta_string)-3):
        seq = delta_string[j:j+4]
        if seq not in seqdict:
            seqdict[seq] = last_digits[i][j+3]
    for seq, value in seqdict.items():
        global_seqdict[seq] += value

print(f'part 2 - {max(global_seqdict.values())}')
