# This is a two player card game
# The game starts with a deck of 52 cards represented as unique integers [1...52]
# The cards are randomly shuffled and then dealt out to both players evenly
# On each turn:
#   - Both players turn over their top-most card
#   - The player with the higher valued card takes the cards and puts them in their scoring pile (scoring 1 point per card)
# This continues until all the players have no cards left
# The player with the highest score wins
# If they have the same number of cards in their win pile, tiebreaker goes to the player with the highest card in their win pile

# Important conditions:
# Entry conditions: 52 numbered cards
# Number of players: 2
# Cards must be shuffled and dealt to players in fashion: one card to player A, one card to player B, etc...
# Game phase:
# -> player A always starts (doesn't matter really)
# -> each player draws the card from the top of their card stack
# -> we compare card values: higher integer wins
# -> Winning player takes both cards to their winning stack
# -> At the end of the round, we count the amount of cards in the winning stack of each player. A game ends with a win or a tiebraker
# -> Tiebreaker: we find which player has a highest cards.

from dataclasses import dataclass
from collections import deque
from random import shuffle
from typing import ClassVar

from .data import GamePlayer
from .game_state import CardGameState, CardGameRound
from .game_history_service import GameHistoryService
from .db.models import CardGameHistoryItem


@dataclass
class CardGameService:
    """A class that contains a toolkit for the card game."""

    DRAW_RANGE: ClassVar[list[int]] = list(range(1, 53))

    def __init__(self):
        raise NotImplementedError(
            (
                "This class cannot be instantiated using a constructor. To start a new game, use initialize_game()"
                " method instead."
            )
        )

    @classmethod
    def initialize_game(cls) -> CardGameState:
        player_a = GamePlayer("Ryan")
        player_b = GamePlayer("Hugh")
        return CardGameState(player_a, player_b)

    @classmethod
    def deal_cards_to_players(cls, state: CardGameState) -> CardGameState:
        if len(cls.DRAW_RANGE) % 2 != 0:
            raise ValueError("The number of cards must be an even number.")

        cards_list = deque(cls.DRAW_RANGE)
        shuffle(cards_list)
        while len(cards_list):
            state.player_a.cards_stack.append(cards_list.pop())
            state.player_b.cards_stack.append(cards_list.pop())
        return state

    @staticmethod
    def is_game_in_progress(state: CardGameState) -> bool:
        """Returns True if the game is still in progress, False otherwise."""
        return not state.is_game_over

    @classmethod
    def play_next_round(cls, state: CardGameState) -> CardGameRound:
        if not state.player_a.cards_stack:
            raise RuntimeError("This game has ended, it is not possible to play another round.")
        return CardGameRound([state.player_a, state.player_b])

    @classmethod
    def apply_round_result(cls, state: CardGameState, round: CardGameRound) -> CardGameState:
        if not state.player_a.cards_stack:
            raise RuntimeError("This game has ended, it is not possible to play another round.")
        winner = round.choose_round_winner()
        state.player_a.cards_stack.pop()
        state.player_b.cards_stack.pop()
        for card in round.get_cards_in_round():
            winner.winning_stack.append(card)
        return state

    @classmethod
    async def get_games_from_history_async(cls) -> list[CardGameHistoryItem]:
        """
        Returns:
            list[CardGameRound]: The current games round history.
        """
        return await GameHistoryService.get_games_from_history_async()

    @classmethod
    async def save_game_to_history_async(cls, state: CardGameState) -> None:
        """
        Saves the current game state to the history.
        """
        await GameHistoryService.save_game_to_history_async(state)
        print(f"Game saved: {state.player_a.name} vs {state.player_b.name}")
