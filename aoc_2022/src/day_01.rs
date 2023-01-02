use std::{
    collections::BinaryHeap,
    fs::File,
    io::{BufRead, BufReader},
    vec,
};

pub(crate) fn run() {
    println!("==== Day 01 ====");
    let mut elf: u64 = 0;

    let mut heap = BinaryHeap::new();

    let file = File::open("inputs/day_01.txt").unwrap();

    for line in BufReader::new(file).lines() {
        let elf_number = line.unwrap();
        if elf_number.trim().len() > 0 {
            elf += elf_number.parse::<u64>().unwrap();
        } else {
            if elf == 0 {
                // println!("No more elves");
                break;
            }
            heap.push(elf);
            elf = 0;
        }
    }

    println!("Part 1: {}", heap.peek().unwrap());

    let top_3 = vec![heap.pop(), heap.pop(), heap.pop()];
    let mut result = 0;
    top_3.iter().for_each(|x| result += x.unwrap());
    println!("Part 2: {}", result);
}
