import time
from collections import Counter

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


def simulate_n_sessions_with_initial_condition(n: int, race_track: RaceTrack):
    winners = Counter()
    for _ in range(n):
        game_session = GameSession(race_track=race_track)
        while not game_session.is_over:
            game_session.step()
        winners[game_session.race_track.winner] += 1
    return winners


if __name__ == "__main__":
    horse_position = make_initial_state()
    horse_position[Horse.H7] = 10
    rt = RaceTrack(horse_position=horse_position)

    start = time.time()
    print(simulate_n_sessions(20000))
    print(simulate_n_sessions_with_initial_condition(20000, race_track=rt))
    end = time.time()
    print(f"Simulation time: {end - start:.2f}")
