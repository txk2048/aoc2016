use std::{collections::HashSet, fs, path::PathBuf};

use clap::{Arg, command, value_parser};

#[derive(Copy, Clone)]
enum Direction {
    North,
    East,
    South,
    West,
}

enum Rotation {
    Clockwise,
    CounterClockwise,
}

struct Instruction {
    rotation: Rotation,
    count: i32,
}

fn parse_rotation(input: &str) -> nom::IResult<&str, Rotation> {
    use nom::Parser;
    use nom::character::one_of;
    use nom::combinator::map;

    map(one_of("LR"), |c| match c {
        'L' => Rotation::CounterClockwise,
        'R' => Rotation::Clockwise,
        _ => unreachable!("invalid rotation"),
    })
    .parse(input)
}

fn parse_instruction(input: &str) -> nom::IResult<&str, Instruction> {
    use nom::Parser;
    use nom::character::complete::i32;
    use nom::combinator::map;
    use nom::sequence::pair;

    map(pair(parse_rotation, i32), |(rotation, count)| Instruction {
        rotation,
        count,
    })
    .parse(input)
}

fn parse_list(input: &str) -> nom::IResult<&str, Vec<Instruction>> {
    use nom::Parser;
    use nom::bytes::complete::tag;
    use nom::multi::separated_list1;

    separated_list1(tag(", "), parse_instruction).parse(input)
}

fn parse_input(input: &str) -> Result<Vec<Instruction>, nom::error::Error<String>> {
    use nom::Finish;
    use nom::Parser;
    use nom::combinator::all_consuming;

    all_consuming(parse_list)
        .parse(input)
        .map_err(|e| e.to_owned())
        .finish()
        .map(|(_, instructions)| instructions)
}

fn solve(instructions: &[Instruction]) -> (i32, Option<i32>) {
    let mut visited = HashSet::new();
    let mut first_visited_twice = None;

    let mut x: i32 = 0;
    let mut y: i32 = 0;
    let mut dir = Direction::North;

    for instruction in instructions {
        use Direction::*;
        use Rotation::*;

        let new_dir = match instruction.rotation {
            Clockwise => match dir {
                North => East,
                East => South,
                South => West,
                West => North,
            },
            CounterClockwise => match dir {
                North => West,
                West => South,
                South => East,
                East => North,
            },
        };

        dir = new_dir;

        for _ in 0..instruction.count {
            visited.insert((x, y));

            match dir {
                North => y += 1,
                East => x += 1,
                South => y -= 1,
                West => x -= 1,
            }

            if first_visited_twice.is_none() && visited.contains(&(x, y)) {
                first_visited_twice = Some((x, y));
            }
        }
    }

    let result1 = x.abs() + y.abs();
    let result2 = first_visited_twice.map(|(x, y)| x.abs() + y.abs());

    (result1, result2)
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
        .expect("could not get input file path");

    let input_contents = fs::read_to_string(input_path).expect("could not read input file");
    let instructions = parse_input(input_contents.trim()).expect("could not parse file");

    let (result1, result2) = solve(&instructions);

    println!("Part 1: {}", result1);
    println!("Part 2: {:?}", result2);
}
