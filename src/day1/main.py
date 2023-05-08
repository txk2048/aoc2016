import argparse
import enum
from dataclasses import dataclass


class Direction(enum.Enum):
    NORTH = enum.auto()
    EAST = enum.auto()
    SOUTH = enum.auto()
    WEST = enum.auto()

    def turn(self, turn):
        if turn == "R":
            if self == Direction.NORTH:
                return Direction.EAST
            elif self == Direction.EAST:
                return Direction.SOUTH
            elif self == Direction.SOUTH:
                return Direction.WEST
            elif self == Direction.WEST:
                return Direction.NORTH
            else:
                raise ValueError("Unrecognised direction")
        elif turn == "L":
            if self == Direction.NORTH:
                return Direction.WEST
            elif self == Direction.EAST:
                return Direction.NORTH
            elif self == Direction.SOUTH:
                return Direction.EAST
            elif self == Direction.WEST:
                return Direction.SOUTH
            else:
                raise ValueError("Unrecognised direction")
        else:
            raise ValueError(f"Invalid turn: {turn}")


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def move(self, direction):
        if direction == Direction.NORTH:
            return Point(self.x, self.y + 1)
        elif direction == Direction.EAST:
            return Point(self.x + 1, self.y)
        elif direction == Direction.SOUTH:
            return Point(self.x, self.y - 1)
        elif direction == Direction.WEST:
            return Point(self.x - 1, self.y)
        else:
            raise ValueError(f"Invalid direction: {direction}")


def part1(instructions):
    point = Point(0, 0)
    current_direction = Direction.NORTH

    for instruction in instructions:
        turn = instruction[0]
        distance = int(instruction[1:])

        current_direction = current_direction.turn(turn)

        for _ in range(distance):
            point = point.move(current_direction)

    return point


def part2(instructions):
    point = Point(0, 0)
    visited = set()

    current_direction = Direction.NORTH
    for instruction in instructions:
        turn = instruction[0]
        distance = int(instruction[1:])

        current_direction = current_direction.turn(turn)

        for _ in range(distance):
            point = point.move(current_direction)
            if point in visited:
                return point
            else:
                visited.add(point)

    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="The input file to read from")
    args = parser.parse_args()

    with open(args.input_file, "r") as f:
        instructions = [d for d in f.read().strip().split(", ")]

    origin = Point(0, 0)

    print(f"Part 1: {part1(instructions).dist(origin)}")
    print(f"Part 2: {part2(instructions).dist(origin)}")


if __name__ == "__main__":
    main()
