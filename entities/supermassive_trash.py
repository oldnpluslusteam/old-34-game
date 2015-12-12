from entities.physical import BigEntity

__author__ = 'moardm'
from fwk.game.entity import GameEntity


@GameEntity.defineClass("supermassive-trash-entity")
class SupermassiveTrash(GameEntity,
                        GameEntity.mixin.Sprite,
                        BigEntity):
    def spawn(self):
        self.radius = 64
        self.mass = 10
        self.sprite = 'rc/img/64x64fg.png'
