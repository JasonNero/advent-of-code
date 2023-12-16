use std::fs;

#[derive(Debug, Clone)]
struct Item {
    label: String,
    focal_length: usize,
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


    result
}

fn solve2(data: &Vec<String>) -> usize {
    // Create an array of length 256 with arrays of usize
    let mut boxes: Vec<Vec<Item>> = vec![vec![]; 256];

    // Loop over the instructions and fill the lens boxes
    for instruction in data {

        // ADD or REPLACE
        if instruction.contains("=") {
            let (label, focal_length) = instruction.split_once("=").unwrap();
            let focal_length: usize = focal_length.parse().unwrap();
            let box_id: usize = custom_hash(&label.to_string());

            let item: Item = Item {
                label: label.to_string(),
                focal_length: focal_length,
            };

            // dbg!(&item);

            let mut found: bool = false;
            for slot_id in 0..boxes[box_id].len() {
                if boxes[box_id][slot_id].label == label {
                    // Replace
                    boxes[box_id][slot_id].focal_length = focal_length;
                    found = true;
                    break;
                }
            }

            if !found {
                // Add
                boxes[box_id].push(item);
            }

        // REMOVE
        } else {
            let label: String = instruction.split_once("-").unwrap().0.to_string();
            let box_id: usize = custom_hash(&label);

            for slot_id in 0..boxes[box_id].len() {
                if boxes[box_id][slot_id].label == label {
                    boxes[box_id].remove(slot_id);
                    break;
                }
            }
        }

    }
    dbg!(&boxes);

    // Calculate the score
    let mut result: usize = 0;
    for box_id in 0..boxes.len() {
        for slot_id in 0..boxes[box_id].len() {
            result += (box_id+1) * (slot_id+1) * boxes[box_id][slot_id].focal_length;
        }
    }

    result
}

fn main() {
    let mut contents: String =
        fs::read_to_string("../15.in").expect("Should have been able to read the file");

    // remove newline at end of file
    contents = contents.trim_end().to_string();

    let data: Vec<String> = parse(&contents);

    println!("Part 1: {}", solve1(&data));
    println!("Part 2: {}", solve2(&data));

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
    fn test_solve2() {
        let contents: String = String::from("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7");
        let testdata: Vec<String> = parse(&contents);
        assert_eq!(solve2(&testdata), 145);
    }
}
