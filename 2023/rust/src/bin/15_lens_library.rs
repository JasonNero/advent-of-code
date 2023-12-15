use std::fs;

fn main() {
    let mut contents: String =
        fs::read_to_string("../15.in").expect("Should have been able to read the file");

    // remove newline at end of file
    contents = contents.trim_end().to_string();

    let data: Vec<String> = parse(&contents);

    solve1(&data);
    solve2(&data);
}

fn parse(data: &String) -> Vec<String> {
    data.split(',')
        .map(|x| x.to_string())
        .collect()
}

fn custom_hash(item: &String) -> usize {
    let mut result: usize = 0;
    for c in item.chars() {
        result += (c as u8) as usize;
        result *= 17;
        result %= 256;
    }
    result
}

fn solve1(data: &Vec<String>) -> usize {
    let hash_values: Vec<usize> = data.iter().map(|x| custom_hash(x)).collect();
    // dbg!(&hash_values);
    let result: usize = hash_values.iter().sum();

    println!("Part 1: {result}");
    result
}

fn solve2(data: &Vec<String>) -> usize {
    0
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_solve1() {
        let contents: String = String::from("HASH");
        let testdata: Vec<String> = parse(&contents);
        assert_eq!(solve1(&testdata), 52);

        let contents: String = String::from("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7");
        let testdata: Vec<String> = parse(&contents);
        assert_eq!(solve1(&testdata), 1320);
    }

    #[test]
    #[ignore]
    fn test_solve2() {
        let contents: String = String::from("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7");
        let testdata: Vec<String> = parse(&contents);
        assert_eq!(solve2(&testdata), 0);
    }
}
