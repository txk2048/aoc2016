import argparse
import hashlib


def part1(door_id):
    password = ""
    index = 0

    print(f"\rPart 1: {'_' * 8}", end="")

    while len(password) < 8:
        hash_input = door_id + str(index)
        hash = hashlib.md5(hash_input.encode("utf-8")).hexdigest()

        if hash.startswith("00000"):
            password += hash[5]
            remaining = 8 - len(password)

            print(f"\rPart 1: {password}{'_' * remaining}", end="")

        index += 1

    print(f"\rPart 1: {password}")


def part2(door_id):
    password = ["_"] * 8
    index = 0

    print(f"\rPart 2: {''.join(password)}", end="")

    while "_" in password:
        hash_input = door_id + str(index)
        hash = hashlib.md5(hash_input.encode("utf-8")).hexdigest()

        if hash.startswith("00000"):
            position = int(hash[5], 16)

            if position < 8 and password[position] == "_":
                password[position] = hash[6]

                print(f"\rPart 2: {''.join(password)}", end="")

        index += 1

    print(f"\rPart 2: {''.join(password)}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input file")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        door_id = f.read().strip()

    part1(door_id)
    part2(door_id)


if __name__ == "__main__":
    main()
