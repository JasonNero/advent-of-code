use ndarray::prelude::*;
use std::{fs, collections::HashMap};


struct Rule {
    part: char,
    condition:
}

struct Workflow {
    id: String,
    rules: Vec<Rule>,
    // parts: HashMap<char, usize>,
}



fn parse(data: &String) -> Grid {
    let (workflows, parts) = data.split_once("\n\n").unwrap();
    let mut workflows: Vec<Workflow> =
}

fn solve1(data: &Grid) -> usize {
    0
}

fn solve2(data: &Grid) -> usize {
    0
}

fn main() {
    let mut contents: String =
        fs::read_to_string("../19.in").expect("Should have been able to read the file");

    // remove newline at end of file
    contents = contents.trim_end().to_string();

    let data = parse(&contents);

    println!("Part 1: {}", solve1(&data));
    println!("Part 2: {}", solve2(&data));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_solve1() {
        let contents: String =
            fs::read_to_string("../19_test.in").expect("Should have been able to read the file");
        let testdata = parse(&contents);
        assert_eq!(solve1(&testdata), 46);
    }

    #[test]
    fn test_solve2() {
        let contents: String =
            fs::read_to_string("../19_test.in").expect("Should have been able to read the file");
        let testdata = parse(&contents);
        assert_eq!(solve2(&testdata), 51);
    }
}
