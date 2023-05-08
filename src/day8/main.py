import argparse
import re


def rect(grid, instruction):
    m = re.match(r"rect (\d+)x(\d+)", instruction)
    width, height = [int(x) for x in m.groups()]

    for i in range(height):
        for j in range(width):
            grid[i][j] = True


def rotate_row(grid, instruction):
    m = re.match(r"rotate row y=(\d+) by (\d+)", instruction)
    row, amount = [int(x) for x in m.groups()]

    for _ in range(amount):
        grid[row] = grid[row][-1:] + grid[row][:-1]


def rotate_column(grid, instruction):
    m = re.match(r"rotate column x=(\d+) by (\d+)", instruction)
    column, amount = [int(x) for x in m.groups()]

    column_data = [grid[i][column] for i in range(len(grid))]

    for _ in range(amount):
        column_data = column_data[-1:] + column_data[:-1]

    for i in range(len(grid)):
        grid[i][column] = column_data[i]


def make_grid(instructions):
    grid = [[False for _ in range(50)] for _ in range(6)]

    for instruction in instructions:
        if instruction.startswith("rect"):
            rect(grid, instruction)
        elif instruction.startswith("rotate row"):
            rotate_row(grid, instruction)
        elif instruction.startswith("rotate column"):
            rotate_column(grid, instruction)

    return grid


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input file")
    args = parser.parse_args()

    with open(args.input, "r") as f:
        instructions = [line.strip() for line in f]

    grid = make_grid(instructions)

    print(f"Part 1: {sum(sum(row) for row in grid)}")

    print("Part 2: ")
    for row in grid:
        line = "".join("#" if cell else " " for cell in row)
        print(line)


if __name__ == "__main__":
    main()
