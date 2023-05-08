import argparse
import json
import os


def part1(lines):
    keypad_file = os.path.join(os.path.dirname(__file__), "keypad1.json")
    with open(keypad_file) as f:
        keypad = json.load(f)

    code = ""
    curr = "5"
    for line in lines:
        for direction in line:
            next_ = keypad[curr][direction]
            if next_:
                curr = next_

        code += curr

    return code


def part2(lines):
    keypad_file = os.path.join(os.path.dirname(__file__), "keypad2.json")
    with open(keypad_file) as f:
        keypad = json.load(f)

    code = ""
    curr = "5"
    for line in lines:
        for direction in line:
            next_ = keypad[curr][direction]
            if next_:
                curr = next_

        code += curr

    return code


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input file")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        lines = [line.strip() for line in f]

    print("Part 1:", part1(lines))
    print("Part 2:", part2(lines))


if __name__ == "__main__":
    main()
