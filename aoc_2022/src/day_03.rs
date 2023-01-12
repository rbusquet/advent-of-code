use itertools::Itertools;
use std::{
    fs::File,
    io::{BufRead, BufReader},
    vec,
};

pub(crate) fn run() {
    println!("==== Day 03 ====");
    let file = File::open("inputs/day_03.txt").unwrap();

    let mut misplaced_priority = 0;
    let mut badges_priority = 0;

    for group in &BufReader::new(file).lines().into_iter().chunks(3) {
        let badges = group
            .map(|line| {
                let line = line.unwrap();
                if line.len() == 0 {
                    return line.clone();
                }
                let (a, b) = line.split_at(line.len() / 2);

                misplaced_priority += find_common(&vec![String::from(a), String::from(b)]);
                line.clone()
            })
            .collect_vec();

        badges_priority += find_common(&badges);
    }
    println!("Part 1: {}", misplaced_priority);
    println!("Part 2: {}", badges_priority);
}

fn find_common(words: &Vec<String>) -> u32 {
    let lower_a: u32 = 'a'.into();
    let upper_a: u32 = 'A'.into();
    let mut common: u32 = 0;
    let mut misplaced_priority = 0;

    let a = words.first().unwrap();

    for ch in a.trim().chars() {
        if ch == '\n' {
            continue;
        }
        let mut is_common = true;
        for word in words[1..].into_iter() {
            is_common &= word.contains(ch);
        }
        if is_common {
            common = ch.into();
            break;
        }
    }
    if common < lower_a {
        let priority = common - upper_a + 26;
        misplaced_priority += priority + 1;
    } else {
        let priority = common - lower_a;
        misplaced_priority += priority + 1;
    }
    misplaced_priority
}
