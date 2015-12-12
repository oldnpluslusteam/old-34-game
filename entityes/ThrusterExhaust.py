__author__ = 'moardm'
from fwk.game.entity import GameEntity
from fwk.ui.console import GAME_CONSOLE


class ThrusterExhaust(GameEntity, GameEntity.mixin.Sprite):
    @staticmethod
    def static_init(game, position):
        self = ThrusterExhaust()
        game.addEntity(self)
        self.position = position
        self.sprite = "rc/img/32x32thruster_exhaust.png"
        return self
