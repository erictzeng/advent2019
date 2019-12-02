import click


def add(int_code, index):
    assert int_code[index] == 1
    a, b, c = int_code[index + 1:index + 4]
    int_code[c] = int_code[a] + int_code[b]


def mul(int_code, index):
    assert int_code[index] == 2
    a, b, c = int_code[index + 1:index + 4]
    int_code[c] = int_code[a] * int_code[b]


def process(int_code, noun=12, verb=2):
    int_code = list(int_code)
    int_code[1] = noun
    int_code[2] = verb
    for index in range(0, len(int_code), 4):
        opcode = int_code[index]
        if opcode == 99:
            break
        else:
            OPCODES[opcode](int_code, index)
    return int_code[0]


def brute(int_code):
    for noun in range(100):
        for verb in range(100):
            if process(int_code, noun=noun, verb=verb) == 19690720:
                return 100 * noun + verb
    return None


OPCODES = {
    1: add,
    2: mul,
}


@click.command()
@click.option('--input', default='../input/day02.txt')
def main(input):
    with open(input, 'r') as f:
        int_code = [int(x) for x in f.readline().strip().split(',')]
    answer = process(int_code)
    answer2 = brute(int_code)
    print(f'Part 1: {answer}')
    print(f'Part 2: {answer2}')


if __name__ == '__main__':
    main()
