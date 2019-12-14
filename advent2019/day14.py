from math import ceil

import click


def parse_input(f):
    reactions = {}
    for line in f:
        ingredients, result = line.strip().split(' => ')
        ingredients = ingredients.split(', ')
        ingredients = dict(parse_component(ingredient) for ingredient in ingredients)
        result, quantity = parse_component(result)
        reactions[result] = (quantity, ingredients)
    return reactions


def parse_component(component):
    amount, name = component.split()
    amount = int(amount)
    return name, amount


def compute_cost(reactions, target, target_quantity, surplus):
    surplus = dict(surplus)
    if target in surplus:
        surplus_amount = surplus[target]
        if surplus_amount >= target_quantity:
            surplus[target] -= target_quantity
            return 0, surplus
        else:
            surplus[target] = 0
            target_quantity -= surplus_amount
    if target == 'ORE':
        return target_quantity, surplus
    amount, recipe = reactions[target]
    total_cost = 0
    num_times = ceil(target_quantity / amount)
    for ingredient, ingredient_quantity in recipe.items():
        cost, surplus = compute_cost(reactions, ingredient, ingredient_quantity * num_times, surplus)
        total_cost += cost
    if target not in surplus:
        surplus[target] = 0
    surplus[target] += num_times * amount - target_quantity
    return total_cost, surplus


def part1(reactions):
    total_cost, surplus = compute_cost(reactions, 'FUEL', 1, {})
    return total_cost


def part2(reactions):
    guess = 1
    goal = 1_000_000_000_000
    increment = 100000
    while increment != 0:
        cost, surplus = compute_cost(reactions, 'FUEL', guess, {})
        while cost < goal:
            guess += increment
            cost, surplus = compute_cost(reactions, 'FUEL', guess, {})
        guess -= increment
        increment = increment // 10
    return guess


@click.command()
@click.option('--input', default='../input/day14.txt')
def main(input):
    with open(input, 'r') as f:
        reactions = parse_input(f)
    answer = part1(reactions)
    print(f'Part 1: {answer}')
    answer2 = part2(reactions)
    print(f'Part 2: {answer2}')


if __name__ == '__main__':
    main()
