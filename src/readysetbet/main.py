import curses
import time

from readysetbet.components import GameSession
from readysetbet.simulation import calculate_probability
from readysetbet.tui import draw_end_race_display, draw_race_board, init_colors

NUM_SIMULATIONS = 1000


def run_animated_race(stdscr, animation_speed: float):
    """Runs a single, animated race using pre-calculated probabilities."""

    init_colors()
    game = GameSession()
    stdscr.nodelay(True)

    while not game.is_over:
        # 0. Calculate probabilities:
        probabilities = calculate_probability(NUM_SIMULATIONS, game)

        # 1. Run one step of the game logic
        game.step()

        # 2. Draw the updated state
        draw_race_board(stdscr, game, probabilities)

        # 3. Control animation speed
        time.sleep(animation_speed)

        # 4. Check for key press (exit logic)
        if stdscr.getch() == ord("q"):
            break

    draw_end_race_display(stdscr, game)


# =========================================================================
# 3. MAIN EXECUTION
# =========================================================================

if __name__ == "__main__":
    ANIMATION_SPEED = 0.95  # Time in seconds between moves

    try:
        # The curses.wrapper handles initialization and safe cleanup of the terminal
        curses.wrapper(lambda stdscr: run_animated_race(stdscr, ANIMATION_SPEED))
    except Exception as e:
        print(f"\nAn error occurred during curses: {e}")
        print(
            "Please ensure your terminal window is large enough and curses is installed correctly."
        )
