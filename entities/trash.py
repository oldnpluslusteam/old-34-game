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

    trashImgs = [
        "trash1.png",
        "trash2.png",
        "trash3.png",
        "trash4.png",
        "trash5.png",
        "trash6.png",
        "trash7.png",
        "trash8.png",
        "trash9.png",
        "trash10.png",
        "trash11.png",
        "trash12.png"
    ]

    def hitBig(self, entity):
        self.suicide()

    def spawn(self):
        self.radius = random.randint(32, 64)
        self.rotation = random.randint(0, 360)
        self._resource = self.radius*0.25
        self.sprite = 'rc/img/' + random.sample(self.trashImgs, 1)[0]
        targetScale = float(self.radius*2)/self.sprite.width
        self.scale = targetScale
        self.spriteAnchor = "center"

    def suicide(self):
        self.game.scheduleAfter(0, self.event('destroy'))

    def on_destroy(self):
        self._sprite = None

    def getResource(self):
        # print("getResources")
        res = self._resource
        self._resource = 0
        self.suicide()
        return res