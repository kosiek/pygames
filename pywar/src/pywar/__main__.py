#!/usr/bin/env python3

import os
import traceback
import asyncio

from django.conf import settings
from django.core.management import execute_from_command_line

MY_HOME = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(MY_HOME, "pywar.sqlite3")


def setup_django():
    settings.configure(
        DEBUG=False,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": DB_PATH,
                "USER": "",
                "PASSWORD": "",
                "HOST": "",
                "PORT": "",
            }
        },
        INSTALLED_APPS=("pywar.db",),
    )
    if not os.path.isfile(DB_PATH):
        execute_from_command_line(
            ["manage.py", "makemigrations", "db"],
        )
        execute_from_command_line(
            ["manage.py", "migrate", "db"],
        )
    execute_from_command_line(
        ["manage.py", "showmigrations", "db"],
    )


# I really hate doing this:
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

# First we must configure Django database, otherwise imports will crash:
setup_django()

from pywar.game_core import CardGameService  # noqa: E402


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
        await asyncio.sleep(0.25)

    winner = game.select_winner()
    print(f"End game winner: {winner}")

    await CardGameService.save_game_to_history_async(game)
    print("Game history saved.")

    if not (games := await CardGameService.get_games_from_history_async()):
        games = []

    print(f"{len(games)} games found in history:")
    for i in games:
        print(
            f"Game ID: {i.game_id}"
            f", Player A: {i.player_a.name!r}"
            f", Player B: {i.player_b.name!r}"
            f", Winner: {i.winner.name!r}.\n"
            f"\tWinner had {i.game_context['player_a_score']} points.\n"
            f"\tLoser had {i.game_context['player_b_score']} points.\n",
        )


if __name__ == "__main__":
    try:
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
        event_loop.run_until_complete(main_game())
    except KeyboardInterrupt:
        print("\r  \nInterrupted. The game result will not apply.\nGoodbye!")
    except Exception:
        print(f"An unhandled error occurred: {traceback.format_exc()}")
        print("The game will now terminate.")
        exit(1)
