import argparse
import re

from collections import Counter
from dataclasses import dataclass


@dataclass
class Room:
    name: str
    sector_id: int
    checksum: str


def is_real_room(room: Room) -> bool:
    # sort the name so Counter insertion order is alphabetical order
    # this means that ties are broken by alphabetical order
    sorted_name = "".join(sorted(room.name))

    counts = Counter(sorted_name)
    checksum = "".join(k for k, v in counts.most_common(5))

    return checksum == room.checksum


def rotate_letter(letter: str, n: int) -> str:
    n %= 26

    old_index = ord(letter) - ord("a")
    new_index = (old_index + n) % 26

    return chr(new_index + ord("a"))


def rotate_string(s: str, n: int) -> str:
    return "".join(rotate_letter(c, n) for c in s)


def part1(rooms: list[Room]) -> int:
    return sum(room.sector_id for room in rooms)


def part2(rooms: list[Room]) -> list:
    for room in rooms:
        decrypted_name = rotate_string(room.name, room.sector_id)
        if "north" in decrypted_name:
            return room.sector_id

    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input file")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        rooms = []

        for line in f:
            m = re.match(r"([a-z-]+)-(\d+)\[([a-z]+)\]", line.strip())
            if not m:
                raise ValueError(f"Invalid input: {line}")

            name = "".join(c for c in m.group(1) if c != "-")
            sector_id = int(m.group(2))
            checksum = m.group(3)

            room = Room(name, sector_id, checksum)
            if is_real_room(room):
                rooms.append(room)

    print(f"Part 1: {part1(rooms)}")
    print(f"Part 2: {part2(rooms)}")


if __name__ == "__main__":
    main()
