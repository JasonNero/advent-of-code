# %%
lines = [l.strip() for l in open("../01.in")]

elves = []
calories = 0
for line in lines:
    if line:
        calories += int(line)
    else:
        elves.append(calories)
        calories = 0

elves.sort()
print(elves[-1])
print(sum(elves[-3:]))
