from entityes.SpaceEntity import StandardSpaceEntity
from entityes.ThrusterExhaust import ThrusterExhaust
from fwk.game.entity import GameEntity
from fwk.ui.console import GAME_CONSOLE


@GameEntity.defineClass("spaceship-entity")
class Spaceship(GameEntity,
                GameEntity.mixin.Sprite,
                GameEntity.mixin.CameraTarget,
                GameEntity.mixin.Movement,
                StandardSpaceEntity):
    # time_for_full_velocity = 3.0
    # full_velocity = 150
    #
    # left_time_for_full_velocity = time_for_full_velocity
    # left_full_velocity = full_velocity
    #
    # standardVelocity = 3000
    def spawn(self):
        self.right_engine = False
        self.left_engine = False
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

    def handle_left_engine(self):
        pass # realized handle left engine

    def handle_right_engine(self):
        pass # realized handle right engine

    def start_left_engine(self):
        pass # realized when start left engine (rotation velocity)

    def start_right_engine(self):
        pass # realized when start right engine (rotation velocity)

    def stop_left_engine(self):
        pass # realized when stop left engine (rotation velocity)

    def stop_right_engine(self):
        pass # realized when stop right engine (rotation velocity)

    # place for handle physic events

    def update(self, dt):
        if (self.left_engine):
            self.handle_left_engine()
        if (self.right_engine):
            self.handle_right_engine()

    def set_right_thruster(self, is_enabled):
        self.right_engine = is_enabled
        if is_enabled:
            self.start_right_engine()
        else:
            self.stop_right_engine()
        GAME_CONSOLE.write("Right thruster is: " + ("On" if is_enabled else "Off"))

    def set_left_thruster(self, is_enabled):
        self.left_engine = is_enabled
        if is_enabled:
            self.start_left_engine()
        else:
            self.stop_left_engine()
        GAME_CONSOLE.write("Left thruster is: " + ("On" if is_enabled else "Off"))