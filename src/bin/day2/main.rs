use clap::{Arg, command, value_parser};

use std::fs;
use std::path::PathBuf;

enum Direction {
    North,
    South,
    West,
    East,
}

fn run_instructions(
    graph: &[Vec<Option<char>>],
    starting_index: (usize, usize),
    instructions: &[Vec<Direction>],
) -> String {
    let mut result = String::new();

    let (mut x, mut y) = starting_index;
    assert!(graph[y][x].is_some());

    let height = graph.len();

    for line in instructions {
        for instruction in line {
            match *instruction {
                Direction::North if y > 0 && graph[y - 1][x].is_some() => y -= 1,
                Direction::South if y + 1 < height && graph[y + 1][x].is_some() => y += 1,
                Direction::West if x > 0 && graph[y][x - 1].is_some() => x -= 1,
                Direction::East if x + 1 < graph[y].len() && graph[y][x + 1].is_some() => x += 1,
                _ => {}
            }
        }

        result.push(graph[y][x].expect("invalid node"));
    }

    result
}

fn part1(instructions: &[Vec<Direction>]) -> String {
    let graph = [
        vec![Some('1'), Some('2'), Some('3')],
        vec![Some('4'), Some('5'), Some('6')],
        vec![Some('7'), Some('8'), Some('9')],
    ];

    run_instructions(&graph, (1, 1), instructions)
}

fn part2(instructions: &[Vec<Direction>]) -> String {
    /*
     *     1
     *   2 3 4
     * 5 6 7 8 9
     *   A B C
     *     D
     */

    #[rustfmt::skip]
    let graph = [
        vec![None, None, Some('1'), None, None],
        vec![None, Some('2'), Some('3'), Some('4'), None],
        vec![Some('5'), Some('6'), Some('7'), Some('8'), Some('9')],
        vec![None, Some('A'), Some('B'), Some('C'), None],
        vec![None, None, Some('D'), None, None],
    ];

    run_instructions(&graph, (0, 2), &instructions)
}

fn main() {
    let args = command!()
        .arg(
            Arg::new("input")
                .required(true)
                .value_parser(value_parser!(PathBuf)),
        )
        .get_matches();

    let input_path = args
        .get_one::<PathBuf>("input")
        .expect("could not get input path");

    let input_contents = fs::read_to_string(input_path).expect("could not read input file");

    let instructions = input_contents
        .trim()
        .lines()
        .map(|line| {
            line.trim()
                .chars()
                .map(|c| match c {
                    'U' => Direction::North,
                    'D' => Direction::South,
                    'L' => Direction::West,
                    'R' => Direction::East,
                    _ => panic!("invalid character"),
                })
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();

    let result1 = part1(&instructions);
    let result2 = part2(&instructions);

    println!("Part 1: {}", result1);
    println!("Part 2: {}", result2);
}

#[cfg(test)]
mod tests {
    use crate::Direction;
    use crate::run_instructions;

    #[test]
    fn test_run_instructions_part1() {
        use Direction::*;

        let graph = [
            vec![Some('1'), Some('2'), Some('3')],
            vec![Some('4'), Some('5'), Some('6')],
            vec![Some('7'), Some('8'), Some('9')],
        ];

        let instructions = [
            vec![North, West, West],
            vec![East, East, South, South, South],
            vec![West, North, East, South, West],
            vec![North, North, North, North, South],
        ];

        let result = run_instructions(&graph, (1, 1), &instructions);
        assert_eq!(result, "1985");
    }

    #[test]
    fn test_run_instructions_part2() {
        use Direction::*;

        /*
         *     1
         *   2 3 4
         * 5 6 7 8 9
         *   A B C
         *     D
         */

        #[rustfmt::skip]
        let graph = [
            vec![None, None, Some('1'), None, None],
            vec![None, Some('2'), Some('3'), Some('4'), None],
            vec![Some('5'), Some('6'), Some('7'), Some('8'), Some('9')],
            vec![None, Some('A'), Some('B'), Some('C'), None],
            vec![None, None, Some('D'), None, None],
        ];

        let instructions = [
            vec![North, West, West],
            vec![East, East, South, South, South],
            vec![West, North, East, South, West],
            vec![North, North, North, North, South],
        ];

        let result = run_instructions(&graph, (0, 2), &instructions);
        assert_eq!(result, "5DB3");
    }
}
