import curses
from dataclasses import dataclass

from readysetbet.components import GameSession, Horse, get_bonus

RSB_TRACK_LENGTHS = {horse: 15 for horse in Horse}
MAX_TRACK_LENGTH = max(RSB_TRACK_LENGTHS.values())

TRACK_START_Y = 4
TRACK_START_X = 8


# Map Horse to Curses Color Pair ID (defined later in init_colors)
HORSE_COLOR_MAP = {
    Horse.H2_3: 1,
    Horse.H4: 1,
    Horse.H10: 1,
    Horse.H11_12: 1,  # Blue (Pair 1)
    Horse.H5: 3,
    Horse.H9: 3,  # Yellow/Orange (Pair 3)
    Horse.H6: 2,
    Horse.H8: 2,  # Red (Pair 2)
    Horse.H7: 4,  # White (Pair 4)
}


def init_colors():
    """Defines the color pairs for the horses."""
    curses.start_color()
    # Pair 1: Blue Horse (2/3, 4, 10, 11/12)
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    # Pair 2: Red Horse (6, 8)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    # Pair 3: Yellow/Orange Horse (5, 9)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    # Pair 4: White Horse (7)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    # Pair 5: Winner/Finish Line (Green)
    curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
    # Pair 6: Red Line (Warning)
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)


def make_last_roll_display(game: GameSession) -> str:
    return f"Roll: {game.current_roll}" if game.current_roll else "Roll: -"


def make_bonus_display(game: GameSession) -> str:
    return (
        f"BONUS: {get_bonus(game.current_roll)} steps"
        if game.dice_history.bonus_advance_check
        else "BONUS: None"
    )


def draw_header(stdscr, game: GameSession):
    stdscr.addstr(0, 0, "--- Ready Set Bet Race Visualization ---", curses.A_BOLD)
    stdscr.addstr(
        1,
        0,
        f"| {make_last_roll_display(game)} | {make_bonus_display(game)} | Press 'q' to quit.",
        curses.color_pair(4),
    )
    stdscr.addstr(2, 0, "-" * (MAX_TRACK_LENGTH + 30))


@dataclass
class HorseTUI:
    track_length: int
    current_pos: int
    # prob_to_win: float
    color_pair_num: int
    color_attr: int
    label: str
    # y: int


def get_horse_info(
    horse: Horse,
    game: GameSession,
) -> HorseTUI:
    color_pair_num = HORSE_COLOR_MAP.get(horse, 4)

    return HorseTUI(
        track_length=RSB_TRACK_LENGTHS[horse],
        current_pos=game.race_track.horse_position[horse],
        # prob_to_win=probabilities[horse],
        color_pair_num=color_pair_num,
        color_attr=curses.color_pair(color_pair_num) | curses.A_BOLD,
        label=f"{horse.name}".replace("_", r"/"),
    )


def draw_horse_tracks(stdscr, game: GameSession):
    horses_to_display = sorted(list(Horse), key=lambda h: h.value)

    for i, horse in enumerate(horses_to_display):
        horse_tui_info = get_horse_info(horse, game)
        y = TRACK_START_Y + i * 2

        # --- 1. Labels and Track ---
        stdscr.addstr(y, 0, horse_tui_info.label, horse_tui_info.color_attr)

        # Draw the dashes for the track
        track_display = "-" * horse_tui_info.track_length
        stdscr.addstr(y, TRACK_START_X, track_display, horse_tui_info.color_attr)

        # Mark the finish line
        stdscr.addstr(
            y, TRACK_START_X + horse_tui_info.track_length, "|", curses.color_pair(5)
        )

        # --- 2. Horse Icon ---
        if horse_tui_info.current_pos < horse_tui_info.track_length:
            icon_attr = horse_tui_info.color_attr
            # Highlight the horse icon if it was the one just moved
            if horse == Horse(game.current_roll):
                icon_attr = horse_tui_info.color_attr | curses.A_REVERSE

            stdscr.addstr(
                y, TRACK_START_X + horse_tui_info.current_pos, "🐴", icon_attr
            )
        else:
            # Draw winner icon
            stdscr.addstr(
                y,
                TRACK_START_X + horse_tui_info.track_length,
                "🏆",
                curses.color_pair(5) | curses.A_REVERSE,
            )


def draw_end_race_display(stdscr, game: GameSession):
    # --- End of Race Display ---
    if game.race_track.winner:
        stdscr.addstr(
            MAX_TRACK_LENGTH + 12,
            0,
            f"RACE OVER! WINNER: {game.race_track.winner.name}!",
            curses.A_BOLD | curses.color_pair(5),
        )
    else:
        stdscr.addstr(MAX_TRACK_LENGTH + 12, 0, "Race Interrupted.", curses.A_BOLD)

    stdscr.addstr(MAX_TRACK_LENGTH + 13, 0, "Press any key to exit.")
    stdscr.nodelay(False)
    stdscr.getch()


def draw_probility_board(stdscr, game: GameSession, probabilities: dict):
    horses_to_display = sorted(list(Horse), key=lambda h: h.value)
    for i, horse in enumerate(horses_to_display):
        y = TRACK_START_Y + i * 2
        horse_tui_info = get_horse_info(horse, game)
        annotation_x = TRACK_START_X + MAX_TRACK_LENGTH + 4
        stdscr.addstr(
            y,
            annotation_x,
            f"P(Win): {probabilities[horse]:.2%}",
            horse_tui_info.color_attr,
        )


def draw_race_board(stdscr, game: GameSession, probabilities: dict):
    """Draws the current state of the race and annotations."""
    stdscr.clear()

    # 0. Header and State Info
    draw_header(stdscr, game)
    # Iterate through all horses in a standard display order
    draw_horse_tracks(stdscr, game)

    # horses_to_display = sorted(list(Horse), key=lambda h: h.value)
    # for i, horse in enumerate(horses_to_display):

    # --- 3. Annotated Probability ---
    draw_probility_board(stdscr, game, probabilities)

    stdscr.refresh()
