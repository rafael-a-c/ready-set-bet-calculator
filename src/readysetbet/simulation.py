import time
from collections import Counter
from copy import deepcopy

from readysetbet.components import GameSession, Horse, RaceTrack, make_initial_state


def play_one_session() -> Horse | None:
    game_session = GameSession()
    while not game_session.is_over:
        game_session.step()
    return game_session.race_track.winner


def simulate_n_sessions(n: int) -> Counter:
    winners = Counter()
    for _ in range(n):
        game_session = GameSession()
        while not game_session.is_over:
            game_session.step()
        winners[game_session.race_track.winner] += 1
    return winners


def simulate_n_sessions_with_initial_condition(
    n: int, game_session: GameSession
) -> Counter:
    winners = Counter()
    for _ in range(n):
        game_copy = deepcopy(game_session)
        while not game_copy.is_over:
            game_copy.step()
        winners[game_copy.race_track.winner] += 1
    return winners


def calculate_probability(n: int, game_session: GameSession) -> dict:
    winners = simulate_n_sessions_with_initial_condition(n, game_session)
    probs = {horse: 0 for horse in Horse}
    probs.update({horse: winners[horse] / n for horse in winners})
    return probs


if __name__ == "__main__":
    horse_position = make_initial_state()
    horse_position[Horse.H7] = 5
    rt = RaceTrack(horse_position=horse_position)

    start = time.time()
    # print(simulate_n_sessions(10000))
    print(simulate_n_sessions_with_initial_condition(10000, race_track=rt))

    print(calculate_probability(10000, game_session=rt))
    end = time.time()
    print(f"Simulation time: {end - start:.2f}")
