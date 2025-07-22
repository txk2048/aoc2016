use clap::{Arg, command, value_parser};

use std::fs;
use std::path::PathBuf;

struct Triangle {
    a: u32,
    b: u32,
    c: u32,
}

impl Triangle {
    pub fn is_possible(&self) -> bool {
        let ab = self.a + self.b > self.c;
        let bc = self.b + self.c > self.a;
        let ac = self.a + self.c > self.b;

        ab && bc && ac
    }
}

fn parse_input(input: &str) -> Option<Vec<Vec<u32>>> {
    let grid = input
        .trim()
        .lines()
        .map(|line| {
            line.split(' ')
                .filter(|part| part.len() != 0)
                .map(|n| n.parse::<u32>())
                .collect::<Result<Vec<_>, _>>()
        })
        .collect::<Result<Vec<Vec<u32>>, _>>()
        .ok()?;

    let all_rows_length_equal_3 = grid.iter().all(|r| r.len() == 3);
    let height_multiple_of_3 = grid.len() % 3 == 0;

    // invalid input
    if !all_rows_length_equal_3 || !height_multiple_of_3 {
        return None;
    }

    Some(grid)
}

fn part1(grid: &Vec<Vec<u32>>) -> usize {
    grid.iter()
        .map(|row| {
            let a = row[0];
            let b = row[1];
            let c = row[2];

            Triangle { a, b, c }
        })
        .filter(|t| t.is_possible())
        .count()
}

fn part2(grid: &Vec<Vec<u32>>) -> usize {
    let mut total = 0;

    for i in 0..3 {
        let column: Vec<_> = grid.iter().map(|r| r[i]).collect();
        let triangles = column.chunks_exact(3).map(|chunk| {
            let a = chunk[0];
            let b = chunk[1];
            let c = chunk[2];

            Triangle { a, b, c }
        });

        total += triangles.filter(|t| t.is_possible()).count();
    }

    total
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
    let grid = parse_input(&input_contents).expect("could not parse input");

    let result1 = part1(&grid);
    let result2 = part2(&grid);

    println!("Part 1: {}", result1);
    println!("Part 2: {}", result2);
}

#[cfg(test)]
mod tests {
    use crate::Triangle;
    use crate::parse_input;

    #[test]
    fn test_triangle_impossible() {
        let triangle = Triangle { a: 5, b: 10, c: 25 };

        assert_eq!(triangle.is_possible(), false);
    }

    #[test]
    fn test_parse_input() {
        let input = concat!(
            "101 301 501\n",
            "102 302 502\n",
            "103 303 503\n",
            "201 401 601\n",
            "202 402 602\n",
            "203 403 603\n",
        );

        let expected_result = vec![
            vec![101, 301, 501],
            vec![102, 302, 502],
            vec![103, 303, 503],
            vec![201, 401, 601],
            vec![202, 402, 602],
            vec![203, 403, 603],
        ];

        let result = parse_input(input).expect("could not parse input");
        assert_eq!(result, expected_result);
    }
}
