import random

from entities.physical import SmallEntity
from entities.space_entity import StandardSpaceEntity
from fwk.game.entity import GameEntity
from fwk.ui.console import GAME_CONSOLE
from fwk.util.graphics import BlitTextureToRect
from fwk.util.rect import Rect


@GameEntity.defineClass("trash-entity")
class Trash(GameEntity,
            GameEntity.mixin.Sprite,
            StandardSpaceEntity,
            SmallEntity):
    _radius = random.randint(32, 64)

    trashImgs = [
        "trash1.png",
        "trash2.png",
        "trash3.png",
        "trash4.png",
        "trash5.png",
        "trash6.png",
        "trash7.png"
    ]

    def hitBig(self, entity):
        self.suicide()

    def spawn(self):
        self.radius = self._radius
        self._resource = self.radius*0.25
        self.sprite = 'rc/img/' + self.trashImgs[random.randint(0, len(self.trashImgs)-1)]
        self.sprite.width = self.radius*2
        self.sprite.height = self.radius*2
        self.spriteAnchor = "center"

    def suicide(self):
        self.game.scheduleAfter(0, self.event('destroy'))

    def getResource(self):
        # print("getResources")
        res = self._resource
        self._resource = 0
        self.suicide()
        return res