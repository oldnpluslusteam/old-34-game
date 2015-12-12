import random

from fwk.game.entity import GameEntity


@GameEntity.defineClass("meteorite-entity")
class Meteorite(GameEntity, GameEntity.mixin.Sprite, GameEntity.mixin.CameraTarget, GameEntity.mixin.Movement):

    def spawn(self):
        pass

    def generateVelocityAndAngle(self, angle = {'start':0, 'end':0}, velocity = {'start':0, 'end':0}):
        pass # handle start angle and velocity
