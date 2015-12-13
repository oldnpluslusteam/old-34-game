from entities.physical import SmallEntity
from entities.space_entity import StandardSpaceEntity
from entities.thruster_exhaust import ThrusterExhaust
from fwk.game.entity import GameEntity
from fwk.ui.console import GAME_CONSOLE
from fwk.util.geometry import directionFromAngle


@GameEntity.defineClass("spaceship-entity")
class Spaceship(GameEntity,
                GameEntity.mixin.Sprite,
                GameEntity.mixin.CameraTarget,
                StandardSpaceEntity,
                SmallEntity):

    _standardAngleVelocity = 10
    _standardVelocity = 1

    def hitBig(self, entity):
        GAME_CONSOLE.write("DIED!!!")

    def hitSmall(self, entity):
        if (entity != self):
            self.change_fuel(entity.getResource())

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
        thruster_exhaust_left = ThrusterExhaust()
        thruster_exhaust_left.parent = self
        self.game.addEntity(thruster_exhaust_left)
        thruster_exhaust_left.animations = "rc/ani/TE_left.json"
        thruster_exhaust_right = ThrusterExhaust()
        thruster_exhaust_right.parent = self
        self.game.addEntity(thruster_exhaust_right)
        thruster_exhaust_right.animations = "rc/ani/TE_right.json"
        self.thruster_exhaust = [thruster_exhaust_left, thruster_exhaust_right]
        # for future
        # self.health = 100
        self.fuel = 100.0
        self.fuelInSecond = 1.0
        self.mass = 3.0
        self.inertion = 0.9

    def handle_velocity(self, vector, dt):
        v = self.velocity
        self.velocity = v[0] + vector[0]*self._standardVelocity, v[1] + vector[1]*self._standardVelocity

    def handle_left_engine(self, dt):
        self.angularVelocity += self._standardAngleVelocity*dt
        self.handle_velocity(directionFromAngle(self.rotation), dt)
        self.change_fuel(-self.fuelInSecond*dt)

    def handle_right_engine(self, dt):
        self.angularVelocity -= self._standardAngleVelocity*dt
        self.handle_velocity(directionFromAngle(self.rotation), dt)
        self.change_fuel(-self.fuelInSecond*dt)

    def change_fuel(self, diff):
        self.fuel += diff
        if (self.fuel < 0):
            self.fuel = 0
        if (self.fuel > 100):
            self.fuel = 100

    def update(self, dt):
        if (self._left_engine and self.fuel > 0):
            self.handle_left_engine(dt)
        if (self._right_engine and self.fuel > 0):
            self.handle_right_engine(dt)

    def set_right_thruster(self, is_enabled):
        self._right_engine = is_enabled

    def set_left_thruster(self, is_enabled):
        self._left_engine = is_enabled