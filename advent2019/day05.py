import click


def parse_opcode(opcode):
    string_opcode = f'{opcode:05d}'
    c = bool(int(string_opcode[0]))
    b = bool(int(string_opcode[1]))
    a = bool(int(string_opcode[2]))
    opcode = int(string_opcode[3:])
    return opcode, a, b, c



def add(int_code, index, a_i=False, b_i=False, c_i=False):
    assert not c_i
    a = int_code[index + 1] if a_i else int_code[int_code[index + 1]]
    b = int_code[index + 2] if b_i else int_code[int_code[index + 2]]
    c = int_code[index + 3]
    int_code[c] = a + b
    return index + 4


def mul(int_code, index, a_i=False, b_i=False, c_i=False):
    assert not c_i
    a = int_code[index + 1] if a_i else int_code[int_code[index + 1]]
    b = int_code[index + 2] if b_i else int_code[int_code[index + 2]]
    c = int_code[index + 3]
    int_code[c] = a * b
    return index + 4


def store(int_code, index, a_i=False, b_i=False, c_i=False):
    assert not a_i
    a = int(input('INPUT: '))
    int_code[int_code[index + 1]] = a
    return index + 2


def output(int_code, index, a_i=False, b_i=False, c_i=False):
    a = int_code[index + 1]
    if a_i:
        print(a)
    else:
        print(int_code[a])
    return index + 2


def jump_if_true(int_code, index, a_i=False, b_i=False, c_i=False):
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

def jump_if_false(int_code, index, a_i=False, b_i=False, c_i=False):
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

def less_than(int_code, index, a_i=False, b_i=False, c_i=False):
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


def process(int_code):
    int_code = list(int_code)
    index = 0
    while True:
        opcode, a_i, b_i, c_i = parse_opcode(int_code[index])
        if opcode == 99:
            break
        else:
            index = OPCODES[opcode](int_code, index, a_i=a_i, b_i=b_i, c_i=c_i)


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


@click.command()
@click.option('--input', default='../input/day05.txt')
def main(input):
    with open(input, 'r') as f:
        int_code = [int(x) for x in f.readline().strip().split(',')]
    process(int_code)


if __name__ == '__main__':
    main()
