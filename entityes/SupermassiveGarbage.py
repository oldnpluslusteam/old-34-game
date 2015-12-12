__author__ = 'moardm'
from fwk.game.entity import GameEntity


@GameEntity.defineClass("supermassive-garbage-entity")
class SupermassiveGarbage(GameEntity, GameEntity.mixin.Sprite):

    @staticmethod
    def static_init(game, position, sprite, radius, mass):
        self = SupermassiveGarbage()
        game.addEntity(self)
        self.position = position
        self.sprite = sprite

        # for future changes
        self.radius = radius
        self.mass = mass

        return self
