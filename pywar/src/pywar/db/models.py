from typing import Any
from django.db import models


class CardGamePlayerItem(models.Model):
    id = models.UUIDField(
        primary_key=True,
        editable=False,
    )
    name = models.CharField(max_length=100)


class CardGameHistoryItem(models.Model):
    game_id = models.UUIDField(
        primary_key=True,
        editable=False,
    )
    player_a = models.ForeignKey(
        CardGamePlayerItem,
        related_name="games_as_player_a",
        on_delete=models.CASCADE,
    )
    player_b = models.ForeignKey(
        CardGamePlayerItem,
        related_name="games_as_player_b",
        on_delete=models.CASCADE,
    )
    winner = models.ForeignKey(
        CardGamePlayerItem,
        related_name="won_games",
        on_delete=models.CASCADE,
    )
    game_context: dict[str, Any] = models.JSONField(  # type: ignore[assignment, reportUnknownVariableType]
        default=dict,
    )
