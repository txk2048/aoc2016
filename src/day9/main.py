import argparse
import itertools


def decompress(s, recurse):
    length = 0

    chars = iter(s)
    for c in chars:
        if c == "(":
            marker = itertools.takewhile(lambda x: x != ")", chars)
            num_chars, times = [int(x) for x in "".join(marker).split("x")]

            affected = "".join(itertools.islice(chars, num_chars))

            if recurse:
                length += decompress(affected, True) * times
            else:
                length += num_chars * times
        else:
            length += 1

    return length


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input file")
    args = parser.parse_args()

    with open(args.input) as f:
        s = f.read().strip()

    print("Part 1:", decompress(s, False))
    print("Part 2:", decompress(s, True))


if __name__ == "__main__":
    main()
