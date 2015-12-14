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
        "supermassive-trash4.png",
        "supermassive-trash5.png",
        "trash4.png",
        "trash5.png"
    ]

    def spawn(self):
        self.radius = random.randint(200, 270)
        self.mass = 0.12*self.radius
        self.sprite = 'rc/img/' + random.sample(self.supermassive_trash_imgs, 1)[0]
        targetScale = float(self.radius*2)/self.sprite.width
        self.scale = targetScale
        self.spriteAnchor = "center"
