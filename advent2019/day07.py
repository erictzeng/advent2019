import click
from itertools import permutations


def parse_opcode(opcode):
    string_opcode = f'{opcode:05d}'
    c = bool(int(string_opcode[0]))
    b = bool(int(string_opcode[1]))
    a = bool(int(string_opcode[2]))
    opcode = int(string_opcode[3:])
    return opcode, a, b, c



def add(int_code, index, a_i=False, b_i=False, c_i=False, inputs=None):
    assert not c_i
    a = int_code[index + 1] if a_i else int_code[int_code[index + 1]]
    b = int_code[index + 2] if b_i else int_code[int_code[index + 2]]
    c = int_code[index + 3]
    int_code[c] = a + b
    return index + 4


def mul(int_code, index, a_i=False, b_i=False, c_i=False, inputs=None):
    assert not c_i
    a = int_code[index + 1] if a_i else int_code[int_code[index + 1]]
    b = int_code[index + 2] if b_i else int_code[int_code[index + 2]]
    c = int_code[index + 3]
    int_code[c] = a * b
    return index + 4


def store(int_code, index, a_i=False, b_i=False, c_i=False, inputs=None):
    assert not a_i
    a = inputs.pop(0)
    #a = int(input('INPUT: '))
    int_code[int_code[index + 1]] = a
    return index + 2


def output(int_code, index, a_i=False, b_i=False, c_i=False, inputs=None):
    assert not a_i
    a = int_code[index + 1]
    return index + 2, a if a_i else int_code[a]


def jump_if_true(int_code, index, a_i=False, b_i=False, c_i=False, inputs=None):
    a = int_code[index + 1]
    if not a_i:
        a = int_code[a]
    b = int_code[index + 2]
    if not b_i:
        b = int_code[b]
    if a == 0:
        return index + 3
    else:
        return b

def jump_if_false(int_code, index, a_i=False, b_i=False, c_i=False, inputs=None):
    a = int_code[index + 1]
    if not a_i:
        a = int_code[a]
    b = int_code[index + 2]
    if not b_i:
        b = int_code[b]
    if a != 0:
        return index + 3
    else:
        return b

def less_than(int_code, index, a_i=False, b_i=False, c_i=False, inputs=None):
    assert not c_i
    a = int_code[index + 1]
    if not a_i:
        a = int_code[a]
    b = int_code[index + 2]
    if not b_i:
        b = int_code[b]
    c = int_code[index + 3]
    if a < b:
        int_code[c] = 1
    else:
        int_code[c] = 0
    return index + 4


def process(int_code, inputs):
    int_code = list(int_code)
    index = 0
    outputs = []
    while True:
        opcode, a_i, b_i, c_i = parse_opcode(int_code[index])
        if opcode == 99:
            break
        elif opcode == 4:
            index, result = OPCODES[opcode](int_code, index, a_i=a_i, b_i=b_i, c_i=c_i, inputs=inputs)
            outputs.append(result)
        else:
            index = OPCODES[opcode](int_code, index, a_i=a_i, b_i=b_i, c_i=c_i, inputs=inputs)
    return outputs


def process_continuous(int_code, index, inputs):
    int_code = list(int_code)
    outputs = []
    while True:
        opcode, a_i, b_i, c_i = parse_opcode(int_code[index])
        if opcode == 99:
            break
        elif opcode == 3 and not inputs:
            return False, (int_code, index), outputs
        elif opcode == 4:
            index, result = OPCODES[opcode](int_code, index, a_i=a_i, b_i=b_i, c_i=c_i, inputs=inputs)
            outputs.append(result)
        else:
            index = OPCODES[opcode](int_code, index, a_i=a_i, b_i=b_i, c_i=c_i, inputs=inputs)
    return True, None, outputs


def equals(int_code, index, a_i=False, b_i=False, c_i=False):
    assert not c_i
    a = int_code[index + 1]
    if not a_i:
        a = int_code[a]
    b = int_code[index + 2]
    if not b_i:
        b = int_code[b]
    c = int_code[index + 3]
    if a == b:
        int_code[c] = 1
    else:
        int_code[c] = 0
    return index  +4

OPCODES = {
    1: add,
    2: mul,
    3: store,
    4: output,
    5: jump_if_true,
    6: jump_if_false,
    7: less_than,
    8: equals,
}

def part1(int_code):
    signals = []
    for sequence in permutations(range(5)):
        result = 0
        for elem in sequence:
            result = process(int_code, [elem, result])[0]
        signals.append(result)
    return max(signals)


def part2(int_code):
    signals = []
    for sequence in permutations(range(5, 10)):
        codes = [list(int_code) for _ in range(5)]
        indices = [0] * 5
        inputs = [
            [sequence[0], 0],
            [sequence[1]],
            [sequence[2]],
            [sequence[3]],
            [sequence[4]],
        ]
        halted = [False] * 5
        while not halted[-1]:
            for amplifier in range(5):
                is_halted, state, outputs = process_continuous(codes[amplifier], indices[amplifier], inputs[amplifier])
                next_amp = (amplifier + 1) % 5
                inputs[next_amp].extend(outputs)
                halted[amplifier] = is_halted
                if not is_halted:
                    codes[amplifier], indices[amplifier] = state
        signals.append(inputs[0][-1])
    return max(signals)


@click.command()
@click.option('--input', default='../input/day07.txt')
def main(input):
    with open(input, 'r') as f:
        int_code = [int(x) for x in f.readline().strip().split(',')]
    answer = part1(int_code)
    answer2 = part2(int_code)
    print(f'Part 1: {answer}')
    print(f'Part 2: {answer2}')


if __name__ == '__main__':
    main()
