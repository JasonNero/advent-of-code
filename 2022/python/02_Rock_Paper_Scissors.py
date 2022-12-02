choice_scores = {
    "rock": 1,
    "paper": 2,
    "scissors": 3,
}

win_scores = {
    "won": 6,
    "draw": 3,
    "lost": 0,
}

winning_combinations = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper",
}

losing_combinations = {
    b: a for a, b in winning_combinations.items()
}

mapping_part1 = {
    "A": "rock",
    "B": "paper",
    "C": "scissors",
    "X": "rock",
    "Y": "paper",
    "Z": "scissors",
}

mapping_part2 = {
    "A": "rock",
    "B": "paper",
    "C": "scissors",
    "X": "lost",
    "Y": "draw",
    "Z": "won",
}


def read_data():
    return [
        line.strip().split(" ")
        for line in open("../02.in")
    ]


def remap_strategy(strategy, mapping):
    return [
        (mapping[choice] for choice in line)
        for line in strategy
    ]


def evaluate_line_part1(opponent, choice):
    score = choice_scores[choice]
    if choice == opponent:
        score += win_scores["draw"]
    elif winning_combinations[choice] == opponent:
        score += win_scores["won"]
    else:
        score += win_scores["lost"]

    return score


def evaluate_line_part2(opponent, result):
    if result == "draw":
        choice = opponent
    if result == "won":
        choice = losing_combinations[opponent]
    if result == "lost":
        choice = winning_combinations[opponent]

    return win_scores[result] + choice_scores[choice]


if __name__ == "__main__":
    strategy = read_data()
    
    total_score = 0
    for line in remap_strategy(strategy, mapping_part1):   
        total_score += evaluate_line_part1(*line)
    print(f"Score for part 1: {total_score}")

    total_score = 0
    for line in remap_strategy(strategy, mapping_part2):   
        total_score += evaluate_line_part2(*line)
    print(f"Score for part 2: {total_score}")
