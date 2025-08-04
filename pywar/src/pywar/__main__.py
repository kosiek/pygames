#!/usr/bin/env python3

import traceback
from asyncio import run, sleep

from pywar.game_core import CardGameService


async def main_game():
    game = CardGameService.initialize_game()
    print("Game initialized.")

    game = CardGameService.deal_cards_to_players(game)
    while CardGameService.is_game_in_progress(game):
        print(f"Player A has the following cards: {game.player_a.cards_stack}")
        print(f"Player B has the following cards: {game.player_b.cards_stack}")
        round = CardGameService.play_next_round(game)
        print(round)
        game = CardGameService.apply_round_result(game, round)
        print(f"{round.round_winner.name} has won this round.")
        await sleep(1)

    winner = game.select_winner()
    print(f"End game winner: {winner}")


if __name__ == "__main__":
    try:
        run(main_game())
    except KeyboardInterrupt:
        print("\r  \nInterrupted. The game result will not apply.\nGoodbye!")
    except Exception:
        print(f"An unhandled error occurred: {traceback.format_exc()}")
        print("The game will now terminate.")
        exit(1)

print("HELLO MAIN")
