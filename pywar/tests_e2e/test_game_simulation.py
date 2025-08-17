from pytest import fixture, mark

from pywar.game_core import CardGameService, CardGameState


@fixture
def game() -> CardGameState:
    return CardGameService.initialize_game()


class TestEndToEndGameSimulation:
    """Tests the full runtime of the card game."""

    @mark.asyncio
    @mark.django_db
    async def test_simulate_game(self, game: CardGameState):
        """This is a basic smoke test that simulates a game from start to finish.

        It initializes a game, deals cards to players, plays rounds until the game is over,
        and finally checks if the game history is saved correctly.

        Args:
            game (CardGameState): An instance of CardGameState to simulate the game.
        """
        game = CardGameService.deal_cards_to_players(game)
        while CardGameService.is_game_in_progress(game):
            print(f"Player A has the following cards: {game.player_a.cards_stack}")
            print(f"Player B has the following cards: {game.player_b.cards_stack}")
            round = CardGameService.play_next_round(game)
            print(round)
            game = CardGameService.apply_round_result(game, round)
            print(f"{round.round_winner.name} has won this round.")

        winner = game.select_winner()
        print(f"End game winner: {winner}")

        await CardGameService.save_game_to_history_async(game)
        print("Game history saved.")

        games = await CardGameService.get_games_from_history_async()

        if not games:
            print("No games found in history.")
        else:
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
