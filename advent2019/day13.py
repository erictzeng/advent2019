import click
import numpy as np

from intcode.processor import IntcodeProcessor


def part1(int_code):
    proc = IntcodeProcessor(int_code)
    halted, outputs = proc.run()
    screen = np.zeros((24, 40), dtype=int)
    max_x, max_y = 0, 0
    for i in range(0, len(outputs), 3):
        x, y, tile_id = outputs[i:i+3]
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        screen[y, x] = tile_id
    return (screen == 2).sum()


def part2(int_code, debug=False):
    int_code[0] = 2
    proc = IntcodeProcessor(int_code, inputs=[])
    screen = np.zeros((24, 40), dtype=int)
    score = 0
    inputs = []
    while True:
        halted, outputs = proc.run(inputs=inputs)
        for i in range(0, len(outputs), 3):
            x, y, tile_id = outputs[i:i+3]
            if x == -1 and y == 0:
                score = tile_id
            else:
                screen[y, x] = tile_id
        if (screen == 2).sum() == 0:
            return score
        if debug:
            print_screen(screen)
        inputs = [generate_move(screen)]


def generate_move(screen):
    paddle_pos = np.where(screen == 3)
    ball_pos = np.where(screen == 4)
    if paddle_pos[1][0] < ball_pos[1][0]:
        return 1
    elif paddle_pos[1][0] > ball_pos[1][0]:
        return -1
    else:
        return 0


def print_screen(screen):
    for y in range(screen.shape[0]):
        for x in range(screen.shape[1]):
            print_tile(screen[y, x])
        print()


def print_tile(tile):
    if tile == 0:
        char = ' '
    elif tile == 1:
        char = '#'
    elif tile == 2:
        char = '+'
    elif tile == 3:
        char = '-'
    elif tile == 4:
        char = '*'
    print(char, end='')



@click.command()
@click.option('--input', default='../input/day13.txt')
def main(input):
    with open(input, 'r') as f:
        int_code = [int(x) for x in f.readline().strip().split(',')]
    answer = part1(int_code)
    print(f'Part 1: {answer}')
    answer2 = part2(int_code)
    print(f'Part 2: {answer2}')


if __name__ == '__main__':
    main()
