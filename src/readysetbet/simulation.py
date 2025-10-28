import time
from collections import Counter

from readysetbet.components import GameSession, Horse
from readysetbet.game_loop import loop


def play_one_session() -> Horse | None:
    game_session = GameSession()
    while not game_session.is_over:
        loop(game_session)
    return game_session.race_track.winner


def play_n_sessions(n: int) -> Counter:
    winners = Counter()
    for _ in range(n):
        winners[play_one_session()] += 1
    return winners


if __name__ == "__main__":
    start = time.time()
    play_n_sessions(20000)
    end = time.time()
    print(f"Simulation time: {end - start:.2f}")
