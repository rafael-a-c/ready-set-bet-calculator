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

    H3 = 3
    H4 = 4
    H5 = 5
    H6 = 6
    H7 = 7
    H8 = 8
    H9 = 9
    H10 = 10
    H11 = 11


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


def get_bonus(curr_roll: int, apply_bonus: bool, bonus: dict = BONUS_ADVANCE) -> int:
    if apply_bonus is False:
        return 0
    return bonus[curr_roll]


@dataclass
class RaceTrack:
    horse_position: Counter = field(default_factory=make_initial_state)

    def update_horse_position(self, current_roll: int, apply_bonus: bool):
        bonus_moves = get_bonus(current_roll, apply_bonus)
        self.horse_position[Horse(current_roll)] += 1 + bonus_moves

    @property
    def winning_horse_at(self) -> int:
        horses = self.horse_position
        return horses.most_common(1)[0][1]

    @property
    def winning_horse(self) -> str:
        horses = self.horse_position
        return horses.most_common(1)[0][0].name


@dataclass
class GameSession:
    race_track: RaceTrack = field(default_factory=RaceTrack)
    dice_history: DiceHistory = field(default_factory=DiceHistory)
