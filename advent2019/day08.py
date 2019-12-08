from collections import Counter

import click
import numpy as np
from PIL import Image


def count(pixels, width=25, height=6):
    num_layers = len(pixels) // (width * height)
    counts = [Counter() for _ in range(num_layers)]
    index = 0
    for i in range(num_layers):
        for _ in range(width * height):
            value = pixels[index]
            counts[i][value] += 1
            index += 1
    num_zeros = [counts[i][0] for i in range(num_layers)]
    layer = num_zeros.index(min(num_zeros))
    return counts[layer][1] * counts[layer][2]


def render(pixels, width=25, height=6):
    image = np.empty((6, 25), dtype=int)
    image[...] = 2
    num_layers = len(pixels) // (width * height)
    index = 0
    for i in range(num_layers):
        for y in range(height):
            for x in range(width):
                if image[y, x] == 2 and pixels[index] != 2:
                    image[y, x] = pixels[index]
                index += 1
    assert not (image == 2).any()
    image = image.astype(bool)
    Image.fromarray(image).save('day08_part2.png')



@click.command()
@click.option('--input', default='../input/day08.txt')
def main(input):
    with open(input, 'r') as f:
        pixels = [int(x) for x in f.readline().strip()]
    answer = count(pixels)
    render(pixels)
    print(f'Part 1: {answer}')
    print(f'Part 2 saved to disk as day08_part2.png')


if __name__ == '__main__':
    main()
