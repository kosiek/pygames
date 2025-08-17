from dataclasses import dataclass, field
from .data import GamePlayer, CardValue, PlayerID, PlayerRoundDraw

from typing import Callable


def tiebreaker_by_maximum_card(
    player_a: GamePlayer,
    player_b: GamePlayer,
) -> GamePlayer:
    """When the game is a tie, this function will be used to select a winner.

    It will select a player with the highest card in their winning stack.

    Args:
        player_a (GamePlayer): First player.
        player_b (GamePlayer): Second player.

    Returns:
        GamePlayer: Either player_a or player_b.
    """
    highest_card_player_a = max(player_a.winning_stack)
    highest_card_player_b = max(player_b.winning_stack)
    winning_player = player_a if highest_card_player_a > highest_card_player_b else player_b
    highest_card = max(highest_card_player_a, highest_card_player_b)
    print(f"Player {winning_player} has scored a highest value card ({highest_card})")
    return winning_player


@dataclass
class CardGameState:
    player_a: GamePlayer
    player_b: GamePlayer
    tiebreaker: Callable[[GamePlayer, GamePlayer], GamePlayer] = tiebreaker_by_maximum_card

    def select_winner(self) -> GamePlayer:
        if not self.is_game_over:
            raise RuntimeError("This game is not over yet, it is not possible to select a winner.")

        print(f"{self.player_a.name!r} has {len(self.player_a.winning_stack)} points.")
        print(f"{self.player_b.name!r} has {len(self.player_b.winning_stack)} points.")

        if len(self.player_a.winning_stack) > len(self.player_b.winning_stack):
            return self.player_a
        if len(self.player_a.winning_stack) < len(self.player_b.winning_stack):
            return self.player_b
        if self.is_tiebreak:
            print("Winner will be decided by a tiebreaker:")
            return self.tiebreaker(self.player_a, self.player_b)
        else:  # pragma: no cover
            # Theoretically this is unreachable code and excessive defensive programming.
            # Anyway I'll keep it, beceause it's more important for me to document the logic.
            raise ValueError("Game is a unsolvable tie, no winner can be selected.")

    @property
    def is_game_over(self) -> bool:
        return not (self.player_a.cards_stack and self.player_b.cards_stack)

    @property
    def is_tiebreak(self) -> bool:
        return len(self.player_a.winning_stack) == len(self.player_b.winning_stack)


@dataclass
class CardGameRound:
    _players_list: list[GamePlayer]

    players: dict[PlayerID, GamePlayer] = field(init=False)
    draw: list[PlayerRoundDraw] = field(init=False)
    round_winner: GamePlayer = field(init=False)

    def __post_init__(self) -> None:
        self.players = {player.id: player for player in self._players_list}
        self.draw = [
            PlayerRoundDraw(player.id, player.cards_stack[-1]) for player in self._players_list
        ]

    def get_cards_in_round(self) -> list[CardValue]:
        """
        Returns:
            list[CardValue]: a list of card values drawn in this round.
        """
        return [draw.card_value for draw in self.draw]

    def choose_round_winner(self) -> GamePlayer:
        """
        Returns:
            GamePlayer: a winning player of this round.
        """
        winning_card = max(self.draw, key=lambda i: i.card_value)
        self.round_winner = self.players[winning_card.player_id]
        return self.round_winner

    def __str__(self):
        info = "Round: "
        for player_draw in self.draw:
            info += f"Player '{self.players[player_draw.player_id].name}' drew {player_draw.card_value}. "
        return info
