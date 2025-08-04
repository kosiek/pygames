#!/usr/bin/env python3
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
from asyncio import sleep, run
from dataclasses import dataclass, field
from collections import deque
from random import shuffle
from uuid import UUID, uuid4
import traceback

CardValue = int
PlayerID = UUID


@dataclass
class GamePlayer:
    name: str
    id: PlayerID = field(default_factory=uuid4)
    winning_stack: deque[CardValue] = field(default_factory=deque[CardValue])
    cards_stack: deque[CardValue] = field(default_factory=deque[CardValue])

    def __str__(self):
        return f"<name: {self.name}>"


@dataclass
class CardGameState:
    player_a: GamePlayer
    player_b: GamePlayer

    @staticmethod
    def tiebreaker(player_a: GamePlayer, player_b: GamePlayer) -> GamePlayer:
        highest_card_player_a = max(player_a.winning_stack)
        highest_card_player_b = max(player_b.winning_stack)
        winning_player = player_a if highest_card_player_a > highest_card_player_b else player_b
        highest_card = max(highest_card_player_a, highest_card_player_b)
        print(f"Player {winning_player} has scored a highest value card ({highest_card})")
        return winning_player

    def select_winner(self) -> GamePlayer:
        winning_player = None
        print(f"{self.player_a.name!r} has {len(self.player_a.winning_stack)} points.")
        print(f"{self.player_b.name!r} has {len(self.player_b.winning_stack)} points.")
        if len(self.player_a.winning_stack) == len(self.player_b.winning_stack):
            print("Winner will be decided by a tiebreak:")
            winning_player = CardGameState.tiebreaker(self.player_a, self.player_b)
        elif len(self.player_a.winning_stack) > len(self.player_b.winning_stack):
            winning_player = self.player_a
        else:
            winning_player = self.player_b
        print(f"{winning_player.name!r} won the game.")
        return winning_player


@dataclass
class PlayerRoundDraw:
    player_id: PlayerID
    card_value: CardValue

    def __str__(self):
        return f"Player {self.player_id} drew card {self.card_value}."

    def __gt__(self, other: "PlayerRoundDraw"):
        return self.card_value > other.card_value

    def __eq__(self, other: "PlayerRoundDraw"):
        return self.card_value == other.card_value


@dataclass
class CardGameRound:
    draw: list[PlayerRoundDraw] = field(init=False)
    players: dict[PlayerID, GamePlayer] = field(init=False)
    round_winner: GamePlayer = field(init=False)

    def __init__(self, state: CardGameState) -> None:
        players = [state.player_a, state.player_b]
        self.players = {player.id: player for player in players}
        self.draw = [PlayerRoundDraw(player.id, player.cards_stack[-1]) for player in players]

    def choose_round_winner(self) -> GamePlayer:
        """
        Returns:
            GamePlayer: a winning player of this round.
        """
        winning_card = max(self.draw, key=lambda i: i.card_value)
        self.round_winner = self.players[winning_card.player_id]
        return self.round_winner

    def get_cards_in_round(self) -> list[CardValue]:
        """
        Returns:
            list[CardValue]: a list of card values drawn in this round.
        """
        return [draw.card_value for draw in self.draw]

    def __str__(self):
        info = "Round: "
        for player_draw in self.draw:
            info += f"Player '{self.players[player_draw.player_id].name}' drew {player_draw.card_value}. "
        return info


@dataclass
class CardGameService:
    """A class that contains a toolkit for the card game."""

    DRAW_RANGE = list(range(1, 53))

    def __init__(self):
        raise NotImplementedError(
            (
                "This class cannot be instantiated using a constructor. To start a new game, use initialize_game()"
                " method instead."
            )
        )

    @classmethod
    def initialize_game(cls) -> CardGameState:
        player_a = GamePlayer("Player A")
        player_b = GamePlayer("Player B")
        return CardGameState(player_a, player_b)

    @classmethod
    def deal_cards_to_players(cls, state: CardGameState) -> CardGameState:
        cards_list = deque(cls.DRAW_RANGE)
        shuffle(cards_list)
        while len(cards_list):
            state.player_a.cards_stack.append(cards_list.pop())
            state.player_b.cards_stack.append(cards_list.pop())
        return state

    @staticmethod
    def is_game_in_progress(state: CardGameState) -> bool:
        """Returns True if the game is still in progress, False otherwise."""
        return bool(len(state.player_a.cards_stack) and len(state.player_b.cards_stack))

    @classmethod
    def play_next_round(cls, state: CardGameState) -> CardGameRound:
        if not state.player_a.cards_stack:
            raise RuntimeError("This game has ended, it is not possible to play another round.")
        return CardGameRound(state)

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
