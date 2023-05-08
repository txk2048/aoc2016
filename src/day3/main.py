import argparse
import itertools


# https://docs.python.org/3/library/itertools.html#itertools-recipes
def batched(iterable, n):
    "Batch data into tuples of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch


def part1(triangles):
    count = 0

    for a, b, c in triangles:
        if a + b <= c or a + c <= b or b + c <= a:
            continue

        count += 1

    return count


def part2(data):
    count = 0

    for batch in batched(data, 3):
        for a, b, c in zip(*batch):
            if a + b <= c or a + c <= b or b + c <= a:
                continue

            count += 1

    return count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input file")
    args = parser.parse_args()

    with open(args.input) as f:
        triangles = [[int(n) for n in line.strip().split()] for line in f]

    print("Part 1:", part1(triangles))
    print("Part 2:", part2(triangles))


if __name__ == "__main__":
    main()
