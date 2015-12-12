from entities.space_entity import StandardSpaceEntity
from fwk.game.entity import GameEntity
from fwk.ui.console import GAME_CONSOLE


@GameEntity.defineClass("trash-entity")
class Trash(GameEntity,
            GameEntity.mixin.Sprite,
            GameEntity.mixin.CameraTarget,
            GameEntity.mixin.Movement,
            StandardSpaceEntity):
    pass