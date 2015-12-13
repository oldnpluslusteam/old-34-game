__author__ = 'moardm'
from fwk.game.entity import GameEntity

class ThrusterExhaust(GameEntity, GameEntity.mixin.Attached, GameEntity.mixin.Animation):
    def spawn(self):
        self.attach(self.parent)
        self.animation = 'off'
        return self