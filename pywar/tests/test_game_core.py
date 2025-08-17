from pytest import raises, fixture
from assertpy import assert_that

from typing import Generator, Any

from pywar.game_core import CardGameService, CardGameState


@fixture
def game() -> Generator[CardGameState, Any, Any]:
    original_draw_range = CardGameService.DRAW_RANGE.copy()
    yield CardGameService.initialize_game()
    CardGameService.DRAW_RANGE = original_draw_range


class TestGameCore:
    def test_initialize_game(self, game: CardGameState):
        assert_that(game.player_a).is_not_none()
        assert_that(game.player_b).is_not_none()
        assert_that(game.player_a.name).is_not_none()
        assert_that(game.player_b.name).is_not_none()
        assert_that(game.player_a.name).is_not_empty
        assert_that(game.player_b.name).is_not_empty()
        assert_that(game.player_a.cards_stack).is_empty()
        assert_that(game.player_b.cards_stack).is_empty()
        assert_that(
            game.is_game_over
        ).is_true()  # Game data is literally empty, so it's not in progress

    def test_deal_cards_to_players(self, game: CardGameState):
        state = CardGameService.deal_cards_to_players(game)
        assert_that(state.player_a.cards_stack).is_not_empty()
        assert_that(state.player_b.cards_stack).is_not_empty()

    def test_deal_cards_to_players_fails_on_odd_draw_range(self, game: CardGameState):
        CardGameService.DRAW_RANGE = list(range(1, 54))
        with raises(ValueError, match="number of cards must be an even number"):
            CardGameService.deal_cards_to_players(game)
