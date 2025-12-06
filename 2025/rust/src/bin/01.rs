use std::fs;

const START_POS: isize = 50;

fn part_one(data: &String) -> usize {
    let mut current_pos: isize = START_POS;
    let mut at_zero_count: usize = 0;

    for _line in data.lines() {
        let movement: isize = if _line.starts_with("L") {
            -_line[1..].parse::<isize>().unwrap()
        } else {
            _line[1..].parse::<isize>().unwrap()
        };

        current_pos = (current_pos + movement) % 100;
        if current_pos == 0 {
            at_zero_count += 1;
        }
    }

    at_zero_count
}

fn part_two(data: &String) -> usize {
    let result: usize = 0;

    result
}

fn main() {
    let mut contents: String =
        fs::read_to_string("../01.in").expect("Should have been able to read the file");

    // remove newline at end of file
    contents = contents.trim_end().to_string();

    println!("Part 1: {}", part_one(&contents));
    println!("Part 2: {}", part_two(&contents));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let contents: String = String::from("L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82\n");
        assert_eq!(part_one(&contents), 3);
    }

    #[test]
    fn test_part_two() {
        let contents: String = String::from("");
        assert_eq!(part_two(&contents), 0);
    }
}
