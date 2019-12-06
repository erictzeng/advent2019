from collections import defaultdict

import click


def walk_graph(graph):
    successors = graph['COM']
    depth = 1
    total = 0
    while successors:
        next = []
        for successor in successors:
            total += depth
            next.extend(graph[successor])
        depth += 1
        successors = next
    return total


def orbital_transfer(parents):
    you_trail = []
    node = 'YOU'
    while node != 'COM':
        node = parents[node]
        you_trail.append(node)
    san_trail = []
    node = 'SAN'
    while node != 'COM':
        node = parents[node]
        san_trail.append(node)
    you_trail = you_trail[::-1]
    san_trail = san_trail[::-1]
    for i in range(len(you_trail)):
        if you_trail[i] != san_trail[i]:
            break
    return len(you_trail) - i + len(san_trail) - i


@click.command()
@click.option('--input', default='../input/day06.txt')
def main(input):
    with open(input, 'r') as f:
        successors = defaultdict(list)
        parents = {}
        for line in f:
            a, b = line.strip().split(')')
            successors[a].append(b)
            parents[b] = a
    answer = walk_graph(successors)
    answer2 = orbital_transfer(parents)
    print(f'Part 1: {answer}')
    print(f'Part 2: {answer2}')


if __name__ == '__main__':
    main()
