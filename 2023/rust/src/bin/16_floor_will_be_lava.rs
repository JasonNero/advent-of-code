use ndarray::prelude::*;
use std::{collections::HashSet, fs};

type Grid = Array2<Tile>;
type Ray = Array1<i32>; // y, x, dy, dx

#[derive(Clone, Debug)]
enum Tile {
    Empty,
    HSplit,
    VSplit,
    RMirror,
    LMirror,
}

impl Tile {
    fn from_char(c: char) -> Tile {
        match c {
            '.' => Tile::Empty,
            '-' => Tile::HSplit,
            '|' => Tile::VSplit,
            '/' => Tile::RMirror,
            '\\' => Tile::LMirror,
            _ => panic!("Unknown tile: {}", c),
        }
    }

    fn divert_ray(&self, ray: &Ray) -> Vec<Ray> {
        match self {
            Tile::Empty => vec![ray.clone()],
            Tile::VSplit => {
                if ray[2] != 0 {
                    // hit on the pointy end - continue in the same direction
                    vec![ray.clone()]
                } else {
                    // split into two rays
                    vec![
                        Ray::from_vec(vec![ray[0], ray[1], 1, 0]),
                        Ray::from_vec(vec![ray[0], ray[1], -1, 0]),
                    ]
                }
            }
            Tile::HSplit => {
                if ray[3] != 0 {
                    // hit on the pointy end - continue in the same direction
                    vec![ray.clone()]
                } else {
                    // split into two rays
                    vec![
                        Ray::from_vec(vec![ray[0], ray[1], 0, 1]),
                        Ray::from_vec(vec![ray[0], ray[1], 0, -1]),
                    ]
                }
            }
            Tile::RMirror => {
                if ray[3] != 0 {
                    // coming from left/right
                    vec![Ray::from_vec(vec![ray[0], ray[1], -ray[3], 0])]
                } else {
                    // coming from up/down
                    vec![Ray::from_vec(vec![ray[0], ray[1], 0, -ray[2]])]
                }
            }
            Tile::LMirror => {
                if ray[3] != 0 {
                    // coming from left/right
                    vec![Ray::from_vec(vec![ray[0], ray[1], ray[3], 0])]
                } else {
                    // coming from up/down
                    vec![Ray::from_vec(vec![ray[0], ray[1], 0, ray[2]])]
                }
            }
        }
    }
}

fn parse(data: &String) -> Grid {
    // From string to grid
    let height = data.lines().count();
    let width = data.lines().next().unwrap().len();
    let mut grid: Grid = Array2::from_elem((height, width), Tile::Empty);
    for (y, line) in data.lines().enumerate() {
        for (x, c) in line.chars().enumerate() {
            grid[[y, x]] = Tile::from_char(c);
        }
    }

    grid
}

fn get_starting_ray(grid: &Grid) -> Ray {
    let ray = Ray::from_vec(vec![0, 0, 0, 1]);
    grid[[0, 0]].divert_ray(&ray)[0].to_owned()
}

fn get_initial_rays(grid: &Grid) -> Vec<Ray> {
    let mut rays = Vec::new();
    for y in 0..grid.shape()[0] {
        rays.push(Ray::from_vec(vec![y as i32, 0, 0, 1]));
        rays.push(Ray::from_vec(vec![
            y as i32,
            (grid.shape()[1] - 1) as i32,
            0,
            -1,
        ]));
    }
    for x in 0..grid.shape()[1] {
        rays.push(Ray::from_vec(vec![0, x as i32, 1, 0]));
        rays.push(Ray::from_vec(vec![
            (grid.shape()[0] - 1) as i32,
            x as i32,
            -1,
            0,
        ]));
    }

    for i in 0..rays.len() {
        let evaluated_rays =
            grid[[rays[i][0] as usize, rays[i][1] as usize]].divert_ray(&rays[i]);

        if evaluated_rays.len() > 1 {
            rays[i] = evaluated_rays[0].to_owned();
            rays.push(evaluated_rays[1].to_owned());
        } else {
            rays[i] = evaluated_rays[0].to_owned();
        }
    }

    rays
}

fn get_visited_set(grid: &Grid, mut rays: Vec<Ray>) -> HashSet<Ray> {
    // insert all starting positions as visited
    let mut visited: HashSet<Ray> = HashSet::from_iter(rays.iter().cloned());

    while !rays.is_empty() {
        let ray = rays.pop().unwrap();

        let (mut y, mut x, dy, dx) = (ray[0], ray[1], ray[2], ray[3]);

        x += dx;
        y += dy;

        let new_ray = Ray::from_vec(vec![y, x, dy, dx]);

        if visited.contains(&new_ray) {
            continue;
        } else if y < 0 || y >= grid.shape()[0] as i32 || x < 0 || x >= grid.shape()[1] as i32 {
            continue;
        }

        let evaluated_rays = grid[[y as usize, x as usize]].divert_ray(&new_ray);
        rays.extend(evaluated_rays);

        visited.insert(new_ray);
    }

    visited
}

fn get_num_energized(visited: &HashSet<Ray>) -> usize {
    visited
        .iter()
        .map(|ray| ray.slice(s![..2]).to_owned())
        .collect::<HashSet<Array1<i32>>>()
        .len()
}

fn solve1(data: &Grid) -> usize {
    let starting_ray = get_starting_ray(&data);
    let visited = get_visited_set(&data, vec![starting_ray]);
    let num_energized = get_num_energized(&visited);
    num_energized
}

fn solve2(data: &Grid) -> usize {
    let initial_rays = get_initial_rays(&data);
    let mut max_energized = 0;
    for ray in initial_rays {
        let visited = get_visited_set(&data, vec![ray]);
        let num_energized = get_num_energized(&visited);
        if num_energized > max_energized {
            max_energized = num_energized;
        }
    }

    max_energized
}

fn main() {
    let mut contents: String =
        fs::read_to_string("../16.in").expect("Should have been able to read the file");

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
            fs::read_to_string("../16_test.in").expect("Should have been able to read the file");
        let testdata = parse(&contents);
        assert_eq!(solve1(&testdata), 46);
    }

    #[test]
    fn test_solve2() {
        let contents: String =
            fs::read_to_string("../16_test.in").expect("Should have been able to read the file");
        let testdata = parse(&contents);
        assert_eq!(solve2(&testdata), 51);
    }
}
