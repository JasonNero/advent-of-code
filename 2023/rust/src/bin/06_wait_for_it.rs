use ndarray::prelude::*;
use ndarray::stack;
use std::fs;

fn main() {
    let file_path: &str = "../06.in";

    let contents: String =
        fs::read_to_string(file_path).expect("Should have been able to read the file");

    println!("Read file '{file_path}' with text:\n\n{contents}");

    let lines: Vec<&str> = contents.lines().collect();

    let (times, records) = parse_part1(&lines);
    let part1: u32 = solve_u32(times, records);
    println!("Part 1: {part1}");

    let (times, records) = parse_part2(&lines);
    let part2: u64 = solve_u64(times, records);
    println!("Part 2: {part2}");
}

fn parse_part1(lines: &Vec<&str>) -> (Vec<u32>, Vec<u32>) {
    let times: Vec<u32> = lines[0]
        .split(':')
        .last()
        .unwrap()
        .split_ascii_whitespace()
        .map(|x| x.parse::<u32>().unwrap())
        .collect();

    let records: Vec<u32> = lines[1]
        .split(':')
        .last()
        .unwrap()
        .split_ascii_whitespace()
        .map(|x| x.parse::<u32>().unwrap())
        .collect();

    (times, records)
}

fn parse_part2(lines: &Vec<&str>) -> (Vec<u64>, Vec<u64>) {
    let time: u64 = lines[0]
        .split(':')
        .last()
        .unwrap()
        .replace(" ", "")
        .parse()
        .unwrap();

    let record: u64 = lines[1]
        .split(':')
        .last()
        .unwrap()
        .replace(" ", "")
        .parse()
        .unwrap();

    (vec![time], vec![record])
}

fn solve_u32(times: Vec<u32>, records: Vec<u32>) -> u32 {
    let mut scores: Vec<u32> = Vec::new();

    for (time, record) in times.iter().zip(records.iter()) {
        println!("Time: {}, Record: {}", time, record);

        let min = 0.;
        let max = (*time + 1) as f32 / 2.0;

        let range_up = Array::range(min, max.ceil(), 1.);
        let range_down = Array::range(max.floor() as f32, (*time + 1) as f32, 1.);

        let combinations = stack![Axis(1), range_up, range_down.slice(s![..;-1])];
        let product = combinations.map_axis(Axis(1), |view| view.iter().product::<f32>());

        let mut num_winning: u32 = product.iter().filter(|x| **x > (*record as f32)).count() as u32;

        num_winning *= 2;
        if *time % 2 == 0 {
            num_winning -= 1;
        }

        println!("{num_winning} winning combinations \n\n");
        scores.push(num_winning);
    }

    scores.iter().product()
}


fn solve_u64(times: Vec<u64>, records: Vec<u64>) -> u64 {
    let mut scores: Vec<u64> = Vec::new();

    for (time, record) in times.iter().zip(records.iter()) {
        println!("Time: {}, Record: {}", time, record);

        let min = 0.;
        let max = (*time + 1) as f32 / 2.0;

        let range_up = Array::range(min, max.ceil(), 1.);
        let range_down = Array::range(max.floor() as f32, (*time + 1) as f32, 1.);

        let combinations = stack![Axis(1), range_up, range_down.slice(s![..;-1])];
        let product = combinations.map_axis(Axis(1), |view| view.iter().product::<f32>());

        let mut num_winning: u64 = product.iter().filter(|x| **x > (*record as f32)).count() as u64;

        num_winning *= 2;
        if *time % 2 == 0 {
            num_winning -= 1;
        }

        println!("{num_winning} winning combinations \n\n");
        scores.push(num_winning);
    }

    scores.iter().product()
}

