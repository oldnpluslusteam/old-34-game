import random

from entities.physical import SmallEntity
from entities.space_entity import StandardSpaceEntity
from fwk.game.entity import GameEntity
from fwk.ui.console import GAME_CONSOLE


@GameEntity.defineClass("trash-entity")
class Trash(GameEntity,
            GameEntity.mixin.Sprite,
            StandardSpaceEntity,
            SmallEntity):

    _maxResource = 20
    _minResource = 5

    def spawn(self):
        self._resource = random.randint(self._minResource, self._maxResource)
        self.sprite = 'rc/img/32x32fg.png'

    def getResource(self):
        # print("getResources")
        res = self._resource
        self._resource = 0
        self.game.scheduleAfter(0, self.event('destroy'))
        return res