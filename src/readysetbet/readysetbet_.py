import random
from collections import Counter

# horses = [3, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11]
# bonus = {3:3, 4:3, 5:2, 6:1, 7:0, 8:1, 9:2, 10:3, 11:3}


def is_end_race(race: Counter):
    mc = race.most_common(1)
    if not mc:
        return False
    return mc.pop()[1] == 15


def move_horse():
    horses = {2: 3, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 11}
    dice_roll = random.randint(1, 6) + random.randint(1, 6)
    return horses[dice_roll]


def calculate_steps(h0, h1, h2):
    bonus = {3: 3, 4: 3, 5: 2, 6: 1, 7: 0, 8: 1, 9: 2, 10: 3, 11: 3}
    if h0 != h1 or h0 == h1 == h2:
        return 1
    return 1 + bonus[h0]


def winner_horse():
    race = Counter()
    second_to_last_moved = 0
    last_moved = 0
    while not is_end_race(race):
        horse = move_horse()
        steps = calculate_steps(horse, last_moved, second_to_last_moved)
        race[horse] += steps
        if horse == last_moved == second_to_last_moved:
            second_to_last_moved = 0
        else:
            second_to_last_moved, last_moved = last_moved, horse
    return race.most_common(1).pop()[0]


# print(race.most_common(3))
# print(c_steps)
# print(second_to_last_moved, last_moved, horse)
# print(Counter([move_horse() for _ in range(100)]))
print(Counter([winner_horse() for _ in range(10)]))
