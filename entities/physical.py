from fwk.game.entity import GameEntity
from fwk.util.all import *

SMALL_ENTITY_TAG = 'small-entity'
BIG_ENTITY_TAG = 'big-entity'
PHYSICAL_ENTITY_TAG = 'physical-entity'

REPULSION_CONSTANT = 1500.0
GRAVITY_CONSTANT = 100000.0

def adjustVelocity(small, big, dt):
	v = small.velocity
	dst = distance(big.position, small.position)

	if dst <= (big.radius + small.radius):
		# print 'coll!'
		big.trigger('hitWith', small)
		small.trigger('hitBig', big)

	dx = (big.position[0] - small.position[0]) / dst
	dy = (big.position[1] - small.position[1]) / dst

	dst2 = dst * dst

	m2 = small.mass * big.mass * GRAVITY_CONSTANT

	dv = dx * m2 / dst2, dy * m2 / dst2
	return v[0]+dv[0], v[1]+dv[1]

class SmallEntity(GameEntity.mixin.Movement):
	events = [
		'hitSmall',	# Hit with SmallEntity; hitSmall(self, small)
		'hitBig'	# Hit with BigEntity; hitBig(self, small)
	]

	def spawn(self):
		self.game.setEntityTags(self, SMALL_ENTITY_TAG)
		self.mass = 1.0
		self.inertion = 0.3
		self.radius = 16.0

	def update(self, dt):
		bigs = self.game.getEntitiesByTag(BIG_ENTITY_TAG)
		kinert = self.inertion ** dt

		self.angularVelocity *= kinert

		v = self.velocity
		self.velocity = v[0]*kinert, v[1]*kinert

		for ent in bigs:
			self.velocity = adjustVelocity(self, ent, dt)

		self._checkCollisionToPlayer()

	def _checkCollisionToPlayer(self):
		player = self.game.getEntityById('player')

		if not player:
			return

		if distance(self.position, player.position) < (self.radius + player.radius):
			player.trigger('hitSmall', self)

class BigEntity(GameEntity.mixin.Movement):
	events = [
		'hitWith'	# Hit with SmallEntity; hitWith(self, small)
	]

	def spawn(self):
		self.game.setEntityTags(self, BIG_ENTITY_TAG)
		self.mass = 1.0
		self.radius = 32.0

	def update(self, dt):
		pass



