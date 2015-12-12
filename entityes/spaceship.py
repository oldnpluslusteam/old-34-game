from math import sin

from fwk.game.entity import GameEntity
from fwk.ui.console import GAME_CONSOLE


@GameEntity.defineClass("spaceship-entity")
class Spaceship(GameEntity, GameEntity.mixin.Sprite, GameEntity.mixin.CameraTarget, GameEntity.mixin.Movement):
    time_for_full_velocity = 3.0
    full_velocity = 150

    left_time_for_full_velocity = time_for_full_velocity
    left_full_velocity = full_velocity

    standardVelocity = 3000
    def spawn(self):
        self.right_engine = False
        self.left_engine = False

    def update(self, dt):
        if (self.right_engine):
            v_x = self._velocity_x

    def set_right_thruster(self, is_enabled):
        self.right_engine = is_enabled
        GAME_CONSOLE.write("Right thruster is: " + ("On" if is_enabled else "Off"))

    def set_left_thruster(self, is_enabled):
        self.left_engine = is_enabled
        GAME_CONSOLE.write("Left thruster is: " + ("On" if is_enabled else "Off"))