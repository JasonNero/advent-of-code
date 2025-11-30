import re

let data = readFile("../01.in")
echo data.spl

let remapping = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}


var numbers: seq[int] = @[]
var digits: seq[string] = @[]

for line in data:
    digits = re.findAll(r"\d{1}", line)
    numbers.add(int("".join([digits[0], digits[-1]])))

echo numbers
