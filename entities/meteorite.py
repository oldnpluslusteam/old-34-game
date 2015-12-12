import random

from entities.physical import SmallEntity
from entities.space_entity import StandardSpaceEntity
from fwk.game.entity import GameEntity


@GameEntity.defineClass("meteorite-entity")
class Meteorite(GameEntity,
                GameEntity.mixin.Sprite,
                GameEntity.mixin.CameraTarget,
                StandardSpaceEntity,
                SmallEntity):
    pass