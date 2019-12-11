import click
import numpy as np
from PIL import Image

from intcode.processor import IntcodeProcessor


class Robot:

    def __init__(self, proc, size=100):
        self.proc = proc
        self.board = np.zeros([size, size], dtype=np.bool)
        self.painted = np.zeros([size, size], dtype=np.bool)
        self.pos = (size // 2, size // 2)
        self.direction = np.array([0, -1])

    def turn(self, direction):
        if direction == 0:
            direction = -1
        rot = np.array([[0, -direction], [direction, 0]])
        self.direction = rot.dot(self.direction)
        x, y = self.pos
        self.pos = (x + self.direction[0], y + self.direction[1])

    def run(self, start=0):
        self.board[self.pos] = start
        halted, outputs = self.proc.run([self.board[self.pos]])
        while not halted:
            assert len(outputs) == 2
            color, direction = outputs
            self.board[self.pos] = color
            self.painted[self.pos] = True
            self.turn(direction)
            halted, outputs = self.proc.run([self.board[self.pos]])
        return self.painted.sum()


@click.command()
@click.option('--input', default='../input/day11.txt')
def main(input):
    with open(input, 'r') as f:
        intcode = [int(x) for x in f.readline().strip().split(',')]
    proc = IntcodeProcessor(intcode, inputs=[])
    robot = Robot(proc)
    answer = robot.run()
    print(f'Part 1: {answer}')
    proc = IntcodeProcessor(intcode, inputs=[])
    robot = Robot(proc)
    robot.run(start=1)
    Image.fromarray(robot.board.transpose()).save('day11-part2.png')
    print(f'Part 2 saved to disk as day11_part2.png')


if __name__ == '__main__':
    main()
