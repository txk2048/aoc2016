import argparse

from dataclasses import dataclass
import re


@dataclass
class Bot:
    low: int = None  # if negative, then abs(low) -1 is output bin
    high: int = None  # if negative, then abs(high) -1 is output bin

    chip1: int = None
    chip2: int = None

    def give_chip(self, chip):
        if self.chip1 is None:
            self.chip1 = chip
        elif self.chip2 is None:
            self.chip2 = chip
        else:
            raise Exception("Bot already has two chips")


def process_instructions(instructions):
    bots = {}

    def give_chip(bot_id, chip):
        if bot_id not in bots:
            # dummy low and high data, will be replaced later
            bots[bot_id] = Bot()

        bot = bots[bot_id]
        bot.give_chip(chip)

    # initialisation
    for instruction in instructions:
        if instruction.startswith("value"):
            m = re.match(r"value (\d+) goes to bot (\d+)", instruction)
            chip = int(m.group(1))
            bot_id = int(m.group(2))

            give_chip(bot_id, chip)
        else:
            m = re.match(
                r"bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)",
                instruction,
            )

            bot_id = int(m.group(1))

            low_type = m.group(2)
            low_id = int(m.group(3))

            high_type = m.group(4)
            high_id = int(m.group(5))

            if bot_id not in bots:
                bots[bot_id] = Bot()

            bots[bot_id].low = -low_id - 1 if low_type == "output" else low_id
            bots[bot_id].high = -high_id - 1 if high_type == "output" else high_id

    return bots


def solve(instructions):
    result1 = None

    bots = process_instructions(instructions)
    outputs = {}

    moved = True
    while moved:
        moved = False
        for bot_id, bot in bots.items():
            if bot.chip1 is None or bot.chip2 is None:
                continue

            moved = True

            if bot.chip1 == 17 and bot.chip2 == 61:
                result1 = bot_id

            low = min(bot.chip1, bot.chip2)
            high = max(bot.chip1, bot.chip2)

            bot.chip1 = None
            bot.chip2 = None

            # give low
            if bot.low < 0:
                outputs[abs(bot.low + 1)] = low
            else:
                bots[bot.low].give_chip(low)

            # give high
            if bot.high < 0:
                outputs[abs(bot.high + 1)] = high
            else:
                bots[bot.high].give_chip(high)

            bot.chip1 = None
            bot.chip2 = None

    result2 = outputs[0] * outputs[1] * outputs[2]
    return result1, result2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input file")
    args = parser.parse_args()

    with open(args.input) as f:
        instructions = [line.strip() for line in f]

    result1, result2 = solve(instructions)

    print("Part 1:", result1)
    print("Part 2:", result2)


if __name__ == "__main__":
    main()
