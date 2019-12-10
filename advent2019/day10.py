from collections import Counter
from math import gcd

import click
import numpy as np


def read_board(f):
    board = []
    for line in f:
        row = []
        for character in line.strip():
            if character == '#':
                row.append(1)
            elif character == '.':
                row.append(0)
            else:
                raise ValueError
        board.append(row)
    return np.array(board)


def can_see(board, a, b):
    h, w = board.shape
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    denom = gcd(dx, dy)
    dx = dx // denom
    dy = dy // denom
    x, y = a
    x += dx
    y += dy
    while True:
        if (x, y) == b:
            return True
        elif board[y, x] == 1:
            return False
        x += dx
        y += dy


def check_all(board):
    h, w = board.shape
    counts = Counter()
    for x in range(w):
        for y in range(h):
            for x2 in range(w):
                for y2 in range(h):
                    if x == x2 and y == y2:
                        continue
                    if board[y, x] == 1 and board[y2, x2] == 1 and can_see(board, (x, y), (x2, y2)):
                        counts[(x, y)] += 1
    return max(counts.items(), key=lambda x: x[1])


def collect_slopes(board, coord):
    h, w = board.shape
    right_slopes = {}
    left_slopes = {}
    for x in range(w):
        for y in range(h):
            candidate = (x, y)
            if candidate == coord:
                continue
            dy = y - coord[1]
            dx = x - coord[0]
            if dx == 0:
                slope = float('-inf')
            else:
                slope = dy / dx
            if dx > 0 or (dx == 0 and dy < 0):
                slopes = right_slopes
            elif dx < 0 or (dx == 0 and dy > 0):
                slopes = left_slopes
            if slope in slopes:
                other = slopes[slope]
                # we've seen this slope before, keep the target furthest away from the base
                if abs(x - coord[0]) + abs(y - coord[1]) > abs(other[0] - coord[0]) + abs(other[1] - coord[1]):
                    slopes[slope] = candidate
            else:
                slopes[slope] = candidate
    return right_slopes, left_slopes


def trace(board, a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    denom = gcd(dx, dy)
    dx = dx // denom
    dy = dy // denom
    x, y = a
    x += dx
    y += dy
    while True:
        if board[y, x] == 1:
            return (x, y)
        elif (x, y) == b:
            return None
        x += dx
        y += dy


def vaporize(board, coord, n=200):
    board = board.copy()
    right_slopes, left_slopes = collect_slopes(board, coord)
    history = {}
    vaporized = 0
    while True:
        # right side
        for slopes in [right_slopes, left_slopes]:
            for _, target in sorted(slopes.items()):
                candidate = trace(board, coord, target)
                if candidate is not None:
                    x, y = candidate
                    board[y, x] = 0
                    vaporized += 1
                    history[vaporized] = candidate
                    if vaporized >= n:
                        return history


def part2(board, coord):
    n = 200
    history = vaporize(board, coord, n=n)
    x, y = history[n]
    return 100 * x + y


@click.command()
@click.option('--input', default='../input/day10.txt')
def main(input):
    with open(input, 'r') as f:
        board = read_board(f)
    coord, answer = check_all(board)
    answer2 = part2(board, coord)
    print(f'Part 1: {answer}')
    print(f'Part 2: {answer2}')


if __name__ == '__main__':
    main()
