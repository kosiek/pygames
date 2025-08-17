from collections import deque
from dataclasses import dataclass, field
from uuid import UUID, uuid4


CardValue = int
PlayerID = UUID

PlayerScore = int


@dataclass
class GamePlayer:
    name: str
    id: PlayerID = field(default_factory=uuid4)
    winning_stack: deque[CardValue] = field(default_factory=deque[CardValue])
    cards_stack: deque[CardValue] = field(default_factory=deque[CardValue])

    def score(self) -> PlayerScore:
        return len(self.winning_stack)

    def __str__(self):
        return f"<name: {self.name}>"


@dataclass
class PlayerRoundDraw:
    player_id: PlayerID
    card_value: CardValue

    def __str__(self):
        return f"Player {self.player_id} drew card {self.card_value}."

    def __gt__(self, other: object):
        if not isinstance(other, PlayerRoundDraw):
            raise TypeError(f"Cannot compare PlayerRoundDraw with {type(other).__name__}.")
        return self.card_value > other.card_value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PlayerRoundDraw):
            return False
        return self.card_value == other.card_value and self.player_id == other.player_id


@dataclass
class CardGameHistory:
    id: UUID
    players: dict[PlayerID, GamePlayer]
    result: dict[PlayerID, PlayerScore]
