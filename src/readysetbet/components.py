import random
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum

POSSIBLE_SUMS = list(range(2, 13))
SUM_COUNT = [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]

BONUS_ADVANCE = {3: 3, 4: 3, 5: 2, 6: 1, 7: 0, 8: 1, 9: 2, 10: 3, 11: 3}


class Horse(Enum):
    """
    Represents the unique horses on the track.
    """

    H2_3 = 3
    H4 = 4
    H5 = 5
    H6 = 6
    H7 = 7
    H8 = 8
    H9 = 9
    H10 = 10
    H11_12 = 11


def roll_dice():
    roll_sum = random.choices(POSSIBLE_SUMS, weights=SUM_COUNT)[0]
    if roll_sum in (3, 2):
        return 3
    if roll_sum in (11, 12):
        return 11
    return roll_sum


@dataclass
class DiceHistory:
    was_back2back: bool = field(default=False)
    last_roll: int = field(default=0)

    def update_roll(self, current_roll: int) -> None:
        self.was_back2back = current_roll == self.last_roll and not self.was_back2back
        self.last_roll = current_roll

    @property
    def bonus_advance_check(self):
        """The check only works after update roll"""
        return self.was_back2back


def make_initial_state():
    initial_state = Counter()
    for horse in Horse:
        initial_state[horse] = 0
    return initial_state


def get_bonus(curr_roll: int, bonus: dict = BONUS_ADVANCE) -> int:
    return bonus[curr_roll]


@dataclass
class RaceTrack:
    horse_position: Counter = field(default_factory=make_initial_state)
    winner: Horse | None = None

    def update_horse_position(self, current_roll: int, bonus_moves: int):
        moving_horse = Horse(current_roll)
        self.horse_position[moving_horse] += 1 + bonus_moves
        if self.horse_position[moving_horse] >= 15:
            self.winner = moving_horse


@dataclass
class GameSession:
    race_track: RaceTrack = field(default_factory=RaceTrack)
    dice_history: DiceHistory = field(default_factory=DiceHistory)
    current_roll: int = field(init=False, default=0)

    @property
    def is_over(self):
        return self.race_track.winner is not None

    def step(self):
        self.current_roll = roll_dice()
        self.dice_history.update_roll(self.current_roll)

        apply_bonus = self.dice_history.bonus_advance_check
        bonus_moves = get_bonus(self.current_roll) if apply_bonus else 0
        self.race_track.update_horse_position(self.current_roll, bonus_moves)
