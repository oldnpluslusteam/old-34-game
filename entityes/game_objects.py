from math import sin

from fwk.game.entity import GameEntity
from fwk.ui.console import GAME_CONSOLE


@GameEntity.defineClass("spaceship-entity")
class Spaceship(GameEntity, GameEntity.mixin.Sprite, GameEntity.mixin.CameraTarget, GameEntity.mixin.Movement):
    x = 0

    standardVelocity = 3000
    def spawn(self):
        self.right_engine = False
        self.left_engine = False

    def y(self, x):
        return sin(x)

    def update(self, dt):
        # print(dt)
        self.x += dt
        self.velocity = (dt*self.standardVelocity, self.y(self.x))

    def set_right_thruster(self, is_enabled):
        self.right_engine = is_enabled
        GAME_CONSOLE.write("Right thruster is: " + ("On" if is_enabled else "Off"))

    def set_left_thruster(self, is_enabled):
        self.left_engine = is_enabled
        GAME_CONSOLE.write("Left thruster is: " + ("On" if is_enabled else "Off"))

@GameEntity.defineClass("meteorite-entity")
class Meteorite(GameEntity, GameEntity.mixin.Sprite, GameEntity.mixin.CameraTarget, GameEntity.mixin.Movement):

    def spawn(self):
        pass
