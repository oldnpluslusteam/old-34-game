from entities.physical import BigEntity

__author__ = 'moardm'
from fwk.game.entity import GameEntity


@GameEntity.defineClass("supermassive-trash-entity")
class SupermassiveTrash(GameEntity,
                        GameEntity.mixin.Sprite,
                        BigEntity):
    def spawn(self):
        self.radius = 32
        self.mass = 8.0
        self.sprite = 'rc/img/64x64fg.png'
