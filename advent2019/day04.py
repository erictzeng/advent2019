def two_adjacent(number):
    number = str(number)
    for i in range(len(number) - 1):
        if number[i] == number[i+1]:
            return True
    return False


def increasing(number):
    prev = -1
    for digit in str(number):
        if int(digit) < prev:
            return False
        prev = int(digit)
    return True


def new_two_adjacent(number):
    number = str(number)
    prev = None
    seen = 0
    for digit in number:
        if digit != prev:
            if seen == 2:
                return True
            else:
                prev = digit
                seen = 1
        else:
            seen += 1
    if seen == 2:
        return True
    return False


def main():
    low = 387638
    high = 919123

    count = 0
    count2 = 0
    for num in range(low, high + 1):
        if two_adjacent(num) and increasing(num):
            count += 1
        if new_two_adjacent(num) and increasing(num):
            count2 += 1

    answer = count
    answer2 = count2
    print(f'Part 1: {answer}')
    print(f'Part 2: {answer2}')


if __name__ == '__main__':
    assert new_two_adjacent(112233)
    assert not new_two_adjacent(123444)
    assert new_two_adjacent(111122)
    main()
