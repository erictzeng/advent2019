import click


def iterate_fuel(amount):
    total = 0
    while amount > 0:
        amount = max(amount // 3 - 2, 0)
        total += amount
    return total


@click.command()
@click.option('--input', default='../input/day01.txt')
def main(input):
    with open(input, 'r') as f:
        total = 0
        iterated_total = 0
        for line in f:
            mass = int(line)
            total += mass // 3 - 2
            iterated_total += iterate_fuel(mass)
    print(f'Part 1: {total}')
    print(f'Part 2: {iterated_total}')


if __name__ == '__main__':
    main()