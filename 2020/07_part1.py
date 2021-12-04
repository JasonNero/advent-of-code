# %%
import collections
from pprint import pprint

def build_dict_from_lines(line):
    color_dict = collections.defaultdict(list)
    for line in lines:
        # These can be skipped
        if "no other" in line:
            continue

        color_in = " ".join(line.split(" ")[:2])
        for element in line.split("contain")[1].split(","):
            color_num = element.strip().split(" ")[0]
            color_out = " ".join(element.strip().split(" ")[1:-1])
            color_dict[color_out].append((color_num, color_in))

    return color_dict

with open("07_input.txt", "r") as f:
    lines = f.readlines()

color_dict = build_dict_from_lines(lines)
# pprint(color_dict)
# print(len(color_dict))

# %%
# How many variants are there to get gold bags?
def gather_bags(color_dict, color_set=set(), outer_color="shiny gold"):
    inner_combinations = color_dict[outer_color]
    inner_set = {col for (num, col) in inner_combinations}
    color_set.update(inner_set)
    for inner_color in inner_set:
        gather_bags(color_dict, color_set, inner_color)
    return color_set

result_colors = gather_bags(color_dict)
pprint(result_colors)
print(len(result_colors))
