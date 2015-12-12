from entityes.SpaceEntity import StandardSpaceEntity
from fwk.game.entity import GameEntity
from fwk.ui.console import GAME_CONSOLE


@GameEntity.defineClass("spaceship-entity")
class Trash(GameEntity,
            GameEntity.mixin.Sprite,
            GameEntity.mixin.CameraTarget,
            GameEntity.mixin.Movement,
            StandardSpaceEntity):
    pass