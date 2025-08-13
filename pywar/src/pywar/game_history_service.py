from dataclasses import dataclass
from uuid import UUID, uuid4

from pywar.game_state import CardGameState
from pywar.db.models import CardGameHistoryItem, CardGamePlayerItem

from asgiref.sync import sync_to_async


@dataclass
class GameHistoryService:
    """A service for managing game history."""

    @staticmethod
    async def save_game_to_history_async(state: CardGameState) -> None:
        """
        Saves the game history to the database. The game state object is simplified to only include
        the necessary information for the history record:
        - Player A and Player B names
        - Winner name
        - Extra game context (scores, tiebreaker status).

        Args:
            state (CardGameState): The current game state to save.
        Raises:
            RuntimeError: If the game is not over yet.
        Raises:
            ValueError: If the game is a tie and no winner can be selected.
        """
        players_db = CardGamePlayerItem.objects

        if not await players_db.filter(id=state.player_a.id).aexists():
            player_a = await players_db.acreate(
                id=state.player_a.id,
                name=state.player_a.name,
            )
        else:
            player_a = await players_db.filter(id=state.player_a.id).aget()

        if not await players_db.filter(id=state.player_b.id).aexists():
            player_b = await players_db.acreate(
                id=state.player_b.id,
                name=state.player_b.name,
            )
        else:
            player_b = await players_db.filter(id=state.player_b.id).aget()

        players = [player_a, player_b]
        winner_id = state.select_winner().id
        winner = next(filter(lambda p: p.id == winner_id, players))

        await CardGameHistoryItem.objects.acreate(
            game_id=uuid4(),
            player_a=player_a,
            player_b=player_b,
            winner=winner,
            game_context={
                "player_a_score": state.player_a.score(),
                "player_b_score": state.player_b.score(),
                "is_tiebreak": state.is_tiebreak,
            },
        )
        print(f"Game history saved for {state.player_a.name} vs {state.player_b.name}.")

    @staticmethod
    @sync_to_async
    def get_games_from_history_async() -> list[CardGameHistoryItem]:
        """
        Retrieves all game history records.
        """
        ## TODO: maybe I can get rid of @sync_to_async if I use .filter()?
        data = CardGameHistoryItem.objects.all()
        return list(data)

    @staticmethod
    async def get_game_from_history_async(game_id: UUID) -> CardGameHistoryItem | None:
        """
        Retrieves the game history for a specific game ID.
        """
        try:
            return await CardGameHistoryItem.objects.aget(game_id=game_id)
        except CardGameHistoryItem.DoesNotExist:
            return None

    @staticmethod
    def commit() -> None:
        raise NotImplementedError
