from entities.physical import SmallEntity
from entities.space_entity import StandardSpaceEntity
from entities.thruster_exhaust import ThrusterExhaust
from fwk.game.entity import GameEntity
from fwk.ui.console import GAME_CONSOLE


@GameEntity.defineClass("spaceship-entity")
class Spaceship(GameEntity,
                GameEntity.mixin.Sprite,
                GameEntity.mixin.CameraTarget,
                StandardSpaceEntity,
                SmallEntity):

    _standardAngleVelocity = 100

    # time_for_full_velocity = 3.0
    # full_velocity = 150
    #
    # left_time_for_full_velocity = time_for_full_velocity
    # left_full_velocity = full_velocity
    #
    # standardVelocity = 3000
    def spawn(self):
        self._right_engine = False
        self._left_engine = False
        self.thruster_exhaust = [
            ThrusterExhaust.static_init(
                game=self.game,
                position=self.position),
            ThrusterExhaust.static_init(
                game=self.game,
                position=self.position)]
        # for future
        self.health = 100
        self.fuel = 100

    def handle_left_engine(self, dt = 0):
        self.angularVelocity += self._standardAngleVelocity*dt

    def handle_right_engine(self, dt = 0):
        self.angularVelocity -= self._standardAngleVelocity*dt

    # place for handle physic events

    def update(self, dt):
        if (self._left_engine):
            self.handle_left_engine(dt)
        if (self._right_engine):
            self.handle_right_engine(dt)

    def set_right_thruster(self, is_enabled):
        self._right_engine = is_enabled
        GAME_CONSOLE.write("Right thruster is: " + ("On" if is_enabled else "Off"))

    def set_left_thruster(self, is_enabled):
        self._left_engine = is_enabled
        GAME_CONSOLE.write("Left thruster is: " + ("On" if is_enabled else "Off"))