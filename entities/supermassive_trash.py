from entities.physical import BigEntity

__author__ = 'moardm'
from fwk.game.entity import GameEntity


@GameEntity.defineClass("supermassive-trash-entity")
class SupermassiveTrash(GameEntity,
                        GameEntity.mixin.Sprite,
                        BigEntity):

    @staticmethod
    def static_init(game, position, sprite, radius, mass):
        self = SupermassiveTrash()
        game.addEntity(self)
        self.position = position
        self.sprite = sprite

        # for future changes
        self.radius = radius
        self.mass = mass

        return self
