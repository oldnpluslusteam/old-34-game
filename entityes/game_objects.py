from math import sin

from fwk.game.entity import GameEntity


@GameEntity.defineClass("spaceship-entity")
class Spaceship(GameEntity, GameEntity.mixin.Sprite, GameEntity.mixin.CameraTarget, GameEntity.mixin.Movement):
    rightEngine = False
    leftEngine = False
    x = 0

    standardVelocity = 3000

    def y(self, x):
        return sin(x)

    def update(self, dt):
        print(dt)
        self.x += dt
        self.velocity = (dt*self.standardVelocity, self.y(self.x))