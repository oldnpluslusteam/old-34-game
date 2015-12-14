import pyglet.media

from entities.physical import SmallEntity
from entities.space_entity import StandardSpaceEntity
from entities.teleport import Teleport
from entities.thruster_exhaust import ThrusterExhaust
from fwk.game.entity import GameEntity
from fwk.sound.static import Play
from fwk.util.geometry import directionFromAngle


@GameEntity.defineClass("spaceship-entity")
class Spaceship(GameEntity,
                GameEntity.mixin.Animation,
                GameEntity.mixin.CameraTarget,
                StandardSpaceEntity,
                SmallEntity):

    _standardAngleVelocity = 130
    _standardVelocity = 400

    _maxAngleVelocity = 200
    _maxVelocity = 300

    _fuel = 100.0
    _fuelInSecond = 3.4
    _mass = 3.0
    _inertion = 0.8
    z_index = 1

    def hitBig(self, entity):
        if entity.__class__ != Teleport:
            Play("rc/snd/destroy.wav")
            self.game.ignore("update")
            self.game.trigger("hitBig")
            self._left_tourbin_sound_player.pause()
            self._right_tourbin_sound_player.pause()
        else:
            Play("rc/snd/do_teleport.wav")

    def hitSmall(self, entity):
        try:
            self.change_fuel(entity.getResource())
            Play("rc/snd/collect.wav")
        except:
            pass

    def preload_engine_sounds(self):
        for side in ('right', 'left'):
            p = getattr(Spaceship, '_'+side+'_tourbin_sound_player', None)
            if p is None:
                snd = pyglet.media.load('rc/snd/tourbin-'+side+'.wav', streaming=False)
                p = pyglet.media.Player()
                p.eos_action = p.EOS_LOOP
                p.queue(snd)
                setattr(Spaceship, '_'+side+'_tourbin_sound_player', p)
            p.pause()

    def spawn(self):
        try:
            self._left_tourbin_sound_player.pause()
            self._right_tourbin_sound_player.pause()
        except AttributeError:
            self.preload_engine_sounds()

        self._right_engine = False
        self._left_engine = False

        self.thruster_exhaust_left = ThrusterExhaust()
        self.thruster_exhaust_left.parent = self
        self.game.addEntity(self.thruster_exhaust_left)
        self.thruster_exhaust_left.animations = "rc/ani/TE_left.json"

        self.thruster_exhaust_right = ThrusterExhaust()
        self.thruster_exhaust_right.parent = self
        self.game.addEntity(self.thruster_exhaust_right)
        self.thruster_exhaust_right.animations = "rc/ani/TE_right.json"
        self.inertion = self._inertion

    def handle_velocity(self, vector, dt):
        v = self.velocity
        targetDeltaX = vector[0]*self._standardVelocity*dt
        targetDeltaY = vector[1]*self._standardVelocity*dt
        tmpVelocity = [v[0] + targetDeltaX, v[1] + targetDeltaY]
        if tmpVelocity[0] > self._maxVelocity:
            tmpVelocity[0] = self._maxVelocity
        if tmpVelocity[1] > self._maxVelocity:
            tmpVelocity[1] = self._maxVelocity
        self.velocity = (tmpVelocity[0], tmpVelocity[1])

    def checkVelocity(self):
        v = self.velocity
        tmpVelocity = [v[0], v[1]]
        if tmpVelocity[0] > self._maxVelocity:
            tmpVelocity[0] = self._maxVelocity
        if tmpVelocity[1] > self._maxVelocity:
            tmpVelocity[1] = self._maxVelocity
        self.velocity = (tmpVelocity[0], tmpVelocity[1])

    def handle_angular_velocity(self, delta):
        self.angularVelocity += delta
        if self.angularVelocity > self._maxAngleVelocity:
            self.angularVelocity = self._maxAngleVelocity

    def handle_left_engine(self, dt):
        self.handle_angular_velocity(self._standardAngleVelocity*dt)
        self.handle_velocity(directionFromAngle(self.rotation), dt)
        self.change_fuel(-Spaceship._fuelInSecond*dt)

    def handle_right_engine(self, dt):
        self.handle_angular_velocity(-self._standardAngleVelocity*dt)
        self.handle_velocity(directionFromAngle(self.rotation), dt)
        self.change_fuel(-Spaceship._fuelInSecond*dt)

    def change_fuel(self, diff):
        Spaceship._fuel += diff
        if diff < 0:
            self.game.onFuelSpent(-diff)
        if (Spaceship._fuel < 0):
            Spaceship._fuel = 0
        if (Spaceship._fuel > 100):
            Spaceship._fuel = 100

    def update(self, dt):
        if (self._left_engine and Spaceship._fuel > 0):
            self.handle_left_engine(dt)

        if (self._right_engine and Spaceship._fuel > 0):
            self.handle_right_engine(dt)
        self.checkVelocity()

    def set_right_thruster(self, is_enabled):
        self._right_engine = is_enabled
        if (Spaceship._fuel > 0):
            state = "on" if is_enabled else "off"
        else:
            state = "off"
        self.thruster_exhaust_right.animation = state
        try:
            if self._right_tourbin_sound_player.playing != (is_enabled and Spaceship._fuel > 0):
                if is_enabled:
                    self._right_tourbin_sound_player.play()
                else:
                    self._right_tourbin_sound_player.pause()
        except:
            pass

    def set_left_thruster(self, is_enabled):
        self._left_engine = is_enabled
        if (Spaceship._fuel > 0):
            state = "on" if is_enabled else "off"
        else:
            state = "off"
        self.thruster_exhaust_left.animation = state
        try:
            if self._left_tourbin_sound_player.playing != (is_enabled and Spaceship._fuel > 0):
                if is_enabled:
                    self._left_tourbin_sound_player.play()
                else:
                    self._left_tourbin_sound_player.pause()
        except:
            pass

    def on_configured(self):
        self.animations = "rc/ani/Spaceship_ani.json"
        self.animation = "standard"

    def on_destroy(self):
        self._left_tourbin_sound_player.stop()
        self._right_tourbin_sound_player.stop()