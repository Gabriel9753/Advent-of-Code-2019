import argparse
import os
import re
import sys
from bisect import bisect_left, bisect_right, insort
from collections import OrderedDict, defaultdict, deque, namedtuple
from datetime import datetime
from functools import lru_cache, partial
from heapq import heapify, heappop, heappush
from itertools import chain, combinations, permutations, product
from math import ceil, floor, gcd, inf, lcm, log2, sqrt
from typing import Dict, List, Set, Tuple

import numpy as np
import z3
from more_itertools import chunked, windowed
from rich import print

cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)

from util.general_util import average_time, load_input, timer, write_times_to_readme

sys.setrecursionlimit(5000)

last_dir = str(os.path.basename(os.path.normpath(cur_dir)))
cur_day = re.findall(r"\d+", last_dir)
cur_day = int(cur_day[0]) if len(cur_day) > 0 else datetime.today().day
images_path = os.path.join(par_dir, "images")


@timer(return_time=True)
def preprocess_input(input_data):
    return list(map(int, input_data.split(",")))


@timer(return_time=True)
def task1(day_input):
    day_input[1] = 12
    day_input[2] = 2
    for i in range(0, len(day_input), 4):
        opcode = day_input[i]

        if opcode == 99 or opcode not in (1, 2, 99):
            break

        in1 = day_input[day_input[i + 1]]
        in2 = day_input[day_input[i + 2]]
        out = day_input[i + 3]

        day_input[out] = in1 + in2 if opcode == 1 else in1 * in2
    return day_input[0]


@timer(return_time=True)
def task2(day_input):
    target = 19690720
    for noun, verb in permutations(range(100), 2):
        program = day_input.copy()
        program[1] = noun
        program[2] = verb
        instruction_pointer = 0
        while instruction_pointer < len(program):
            opcode = program[instruction_pointer]

            if opcode == 99:
                break

            in1 = program[program[instruction_pointer + 1]]
            in2 = program[program[instruction_pointer + 2]]
            out = program[instruction_pointer + 3]

            match opcode:
                case 1:
                    program[out] = in1 + in2
                    instruction_pointer += 4
                case 2:
                    program[out] = in1 * in2
                    instruction_pointer += 4
                case _:
                    break
        if program[0] == target:
            return 100 * noun + verb


def main(args):
    if not args.final:
        day_input = load_input(os.path.join(cur_dir, "example_input.txt"))
    else:
        day_input = load_input(os.path.join(cur_dir, "input.txt"))

    day_input, t = preprocess_input(day_input)
    result_task1, time_task1 = task1(day_input.copy())
    result_task2, time_task2 = task2(day_input)

    print(f"\nDay {cur_day}")
    print("------------------")
    print(f"Processing data: {t:.6f} seconds")
    print(f"Task 1: {result_task1} ({time_task1:.6f} seconds)")
    print(f"Task 2: {result_task2} ({time_task2:.6f} seconds)")

    if args.timeit:
        avg_time_task1 = average_time(100, task1, [], day_input)
        avg_time_task2 = average_time(100, task2, [], day_input)
        print("\nAverage times:")
        print(f"Task 1: {avg_time_task1:.6f} seconds")
        print(f"Task 2: {avg_time_task2:.6f} seconds")
        write_times_to_readme(cur_day, avg_time_task1, avg_time_task2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--final", help="Use the final input", action="store_true")
    parser.add_argument("--timeit", help="Average the execution time over 100 runs", action="store_true")
    main(parser.parse_args())
