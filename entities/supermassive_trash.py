import random

from entities.physical import BigEntity

__author__ = 'moardm'
from fwk.game.entity import GameEntity


@GameEntity.defineClass("supermassive-trash-entity")
class SupermassiveTrash(GameEntity,
                        GameEntity.mixin.Sprite,
                        BigEntity):

    supermassive_trash_imgs = [
        "supermassive-trash1.png",
        "supermassive-trash2.png",
        "supermassive-trash3.png",
        "trash4.png",
        "trash5.png"
    ]

    def spawn(self):
        self.radius = random.randint(128, 256)
        self.mass = 0.1*self.radius
        self.sprite = 'rc/img/' + self.supermassive_trash_imgs[random.randint(0, len(self.supermassive_trash_imgs)-1)]
        targetScale = float(self.radius*2)/self.sprite.width
        self.scale = targetScale
        self.spriteAnchor = "center"
