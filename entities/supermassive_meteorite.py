from entities.physical import BigEntity
from entities.space_entity import StandardSpaceEntity
from fwk.game.entity import GameEntity


@GameEntity.defineClass("supermassive-meteorite-entity")
class Meteorite(GameEntity,
                GameEntity.mixin.Sprite,
                GameEntity.mixin.CameraTarget,
                GameEntity.mixin.Movement,
                StandardSpaceEntity,
                BigEntity):
    pass