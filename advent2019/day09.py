import click


from intcode.processor import IntcodeProcessor


@click.command()
@click.option('--input', default='../input/day09.txt')
def main(input):
    with open(input, 'r') as f:
        intcode = [int(x) for x in f.readline().strip().split(',')]
    proc = IntcodeProcessor(intcode, inputs=[1])
    answer = proc.run()[1][0]
    proc.reset(inputs=[2])
    answer2 = proc.run()[1][0]
    print(f'Part 1: {answer}')
    print(f'Part 2: {answer2}')


if __name__ == '__main__':
    main()
