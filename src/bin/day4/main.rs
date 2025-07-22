use clap::{Arg, command, value_parser};
use itertools::Itertools;

use std::fs;
use std::path::PathBuf;

#[derive(Debug, Eq, PartialEq)]
struct Room {
    encrypted_name: String,
    decrypted_name: String,

    sector_id: u32,
    checksum: [char; 5],
}

impl Room {
    fn new(encrypted_name: String, sector_id: u32, checksum: [char; 5]) -> Self {
        let decrypted_name = Self::decrypt_name(&encrypted_name, sector_id);

        Room {
            encrypted_name: encrypted_name.to_owned(),
            decrypted_name,
            sector_id,
            checksum,
        }
    }

    fn is_real(&self) -> bool {
        let mut counts: Vec<_> = self
            .encrypted_name
            .chars()
            .filter(|c| *c != '-')
            .counts()
            .into_iter()
            .collect();

        // sort alphabetically
        counts.sort_by_key(|(c, _)| *c);

        // reverse sort numerically
        counts.sort_by(|(_, c1), (_, c2)| c2.cmp(c1));

        counts
            .iter()
            .map(|(c, _)| c)
            .zip(self.checksum)
            .all(|(computed, checksum)| *computed == checksum)
    }

    fn decrypt_name(name: &str, sector_id: u32) -> String {
        name.chars()
            .map(|c| {
                if c == '-' {
                    return ' ';
                }

                let base = 'a' as u8;

                let idx = (c as u8 - base) as u32;
                let new_idx = ((idx + sector_id) % 26) as u8;

                (new_idx + base) as char
            })
            .collect()
    }

    fn parse<'a>(input: &'a str) -> Result<Room, nom::error::Error<&'a str>> {
        use nom::character::complete::{alpha1, char, one_of, u32};
        use nom::combinator::{all_consuming, map};
        use nom::error::Error;
        use nom::multi::{count, separated_list1};
        use nom::sequence::{delimited, preceded};
        use nom::{Finish, Parser};

        let parse_encrypted_name = map(
            separated_list1(char::<&str, Error<&str>>('-'), alpha1),
            |chunks| chunks.join("-"),
        );

        let parse_checksum = map(
            delimited(
                char('['),
                count(one_of("abcdefghijklmnopqrstuvwxyz"), 5),
                char(']'),
            ),
            |checksum| <[char; 5]>::try_from(checksum).unwrap(),
        );

        let mut parser = all_consuming((
            parse_encrypted_name,
            preceded(char('-'), u32),
            parse_checksum,
        ));

        let result =
            parser
                .parse(input)
                .finish()
                .map(|(_, (encrypted_name, sector_id, checksum))| {
                    Room::new(encrypted_name, sector_id, checksum)
                });

        result
    }
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

    let rooms = input_contents
        .trim()
        .lines()
        .map(|line| Room::parse(line.trim()))
        .collect::<Result<Vec<_>, _>>()
        .expect("could not process input");

    let real_rooms: Vec<Room> = rooms.into_iter().filter(|room| room.is_real()).collect();

    let result1: u32 = real_rooms.iter().map(|room| room.sector_id).sum();
    println!("Part 1: {}", result1);

    let result2: Option<u32> = real_rooms
        .into_iter()
        .filter(|room| room.decrypted_name.contains("object"))
        .next()
        .map(|room| room.sector_id);

    println!("Part 2: {:?}", result2);
}

#[cfg(test)]
mod tests {
    use crate::Room;

    #[test]
    fn test_decrypt_name() {
        let name = "qzmt-zixmtkozy-ivhz";
        let expected_name = "very encrypted name";

        let result = Room::decrypt_name(name, 343);

        assert_eq!(result, expected_name);
    }

    #[test]
    fn test_parse_room() {
        let spec = "aaaaa-bbb-z-y-x-123[abxyz]";
        let expected_room = Room {
            encrypted_name: "aaaaa-bbb-z-y-x".to_owned(),
            decrypted_name: "ttttt uuu s r q".to_owned(),
            sector_id: 123,
            checksum: ['a', 'b', 'x', 'y', 'z'],
        };

        let room = Room::parse(spec).expect("failed to parse");

        assert_eq!(room, expected_room);
    }
}
