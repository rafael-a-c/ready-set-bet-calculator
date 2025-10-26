from readysetbet.components import GameSession, roll_dice


def keep_playing(game_session: GameSession) -> bool:
    return game_session.race_track.winning_horse_at < 15


def loop(game_session: GameSession):
    curr_roll = roll_dice()
    game_session.dice_history.update_roll(curr_roll)

    apply_bonus = game_session.dice_history.bonus_advance_check
    game_session.race_track.update_horse_position(curr_roll, apply_bonus)
