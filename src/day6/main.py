import argparse
from collections import Counter


def decode(messages, most_common):
    columns = zip(*messages)

    message = ""
    for column in columns:
        counter = Counter(column)

        letter = None
        if most_common:
            letter, _ = counter.most_common(1)[0]
        else:
            letter, _ = counter.most_common()[-1]

        message += letter

    return message


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input file")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        messages = [line.strip() for line in f]

    print(f"Part 1: {decode(messages, True)}")
    print(f"Part 2: {decode(messages, False)}")


if __name__ == "__main__":
    main()
