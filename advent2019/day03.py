import click


def wire_to_vertices(wire):
    x, y = 0, 0
    vertices = []
    vertices.append((x, y))
    for instruction in wire:
        direction = instruction[0]
        amount = int(instruction[1:])
        if direction == 'R':
            x += amount
        elif direction == 'L':
            x -= amount
        elif direction == 'U':
            y += amount
        elif direction == 'D':
            y -= amount
        else:
            raise ValueError(direction)
        vertices.append((x, y))
    return vertices


def intersection(segment1, segment2):
    segment1 = list(sorted(segment1))
    segment2 = list(sorted(segment2))
    if segment1[0][0] == segment1[1][0] and segment2[0][0] == segment2[1][0]:
        return None
    if segment1[0][1] == segment1[1][1] and segment2[0][1] == segment2[1][1]:
        return None
    if segment1[0][0] == segment1[1][0]:
        segment1, segment2 = segment2, segment1
    if (segment1[0][0] <= segment2[0][0] <= segment1[1][0]
        and segment2[0][1] <= segment1[0][1] <= segment2[1][1]):
        return segment2[0][0], segment1[0][1]
    return None


def intersection_pt(segment, pt):
    segment = list(sorted(segment))
    return segment[0][0] <= pt[0] <= segment[1][0] and segment[0][1] <= pt[1] <= segment[1][1]

def find_all_intersections(vertices1, vertices2):
    intersections = []
    for i in range(len(vertices1) - 1):
        for j in range(len(vertices2) - 1):
            candidate = intersection(vertices1[i:i + 2], vertices2[j:j + 2])
            if candidate is not None:
                intersections.append(candidate)
    return intersections

def pt_to_dist(pt):
    return abs(pt[0]) + abs(pt[1])

def wire_distance(vertices, pt):
    distance = 0
    for i in range(len(vertices) - 1):
        segment = vertices[i:i + 2]
        if intersection_pt(segment, pt):
            distance += abs(segment[0][0] - pt[0]) + abs(segment[0][1] - pt[1])
            break
        else:
            distance += abs(segment[0][0] - segment[1][0]) + abs(segment[0][1] - segment[1][1])
    else:
        raise ValueError
    return distance


def find_closest_intersection_wire_distance(vertices1, vertices2, intersections):
    wire_distances = [wire_distance(vertices1, pt) + wire_distance(vertices2, pt) for pt in intersections]
    return min(wire_distances)

@click.command()
@click.option('--input', default='../input/day03.txt')
def main(input):
    with open(input, 'r') as f:
        wire1 = f.readline().strip().split(',')
        wire2 = f.readline().strip().split(',')
    vertices1 = wire_to_vertices(wire1)
    vertices2 = wire_to_vertices(wire2)
    intersections = find_all_intersections(vertices1, vertices2)
    answer = min(pt_to_dist(pt) for pt in intersections)
    answer2 = find_closest_intersection_wire_distance(vertices1, vertices2, intersections)
    print(f'Part 1: {answer}')
    print(f'Part 2: {answer2}')


if __name__ == '__main__':
    main()
