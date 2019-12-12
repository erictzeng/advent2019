import click
import numpy as np


def parse_input(f):
    coords = []
    for line in f:
        coords.append([int(comp.split('=')[1]) for comp in line.strip()[:-1].split(',')])
    return coords


def step(coords, velocities):
    # apply gravity
    for i in range(coords.shape[0]):
        velocities[i] += (coords[i] < coords).sum(axis=0)
        velocities[i] -= (coords[i] > coords).sum(axis=0)
    # apply velocity
    coords += velocities
    return coords, velocities


def compute_energy(coords, velocities):
    return (np.abs(coords).sum(1) * np.abs(velocities).sum(1)).sum()


def find_cycle_lengths(coords, velocities):
    coords = coords.copy()
    velocities = velocities.copy()
    cycle_lengths = [None, None, None]
    seen = [set() for _ in range(3)]
    iterations = 0
    while True:
        for dim in range(3):
            if cycle_lengths[dim] is not None:
                continue
            flat = tuple(coords[:, dim].reshape(-1).tolist()) + tuple(velocities[:, dim].reshape(-1).tolist())
            if flat in seen[dim]:
                cycle_lengths[dim] = iterations
                if all(cycle_len is not None for cycle_len in cycle_lengths):
                    return cycle_lengths
            else:
                seen[dim].add(flat)
        coords, velocities = step(coords, velocities)
        iterations += 1


def part1(coords, velocities):
    coords = coords.copy()
    velocities = velocities.copy()
    for _ in range(1000):
        coords, velocities = step(coords, velocities)
    return compute_energy(coords, velocities)


def part2(coords, velocities):
    coords = coords.copy()
    velocities = velocities.copy()
    cycle_lengths = find_cycle_lengths(coords, velocities)
    cycle_lengths = np.array(cycle_lengths, dtype=np.int64)  # avoid integer overflow, lol
    return np.lcm.reduce(cycle_lengths)


@click.command()
@click.option('--input', default='../input/day12.txt')
def main(input):
    with open(input, 'r') as f:
        coords = np.array(parse_input(f))
    velocities = np.zeros_like(coords)
    answer = part1(coords, velocities)
    print(f'Part 1: {answer}')
    answer2 = part2(coords, velocities)
    print(f'Part 2: {answer2}')


if __name__ == '__main__':
    main()
