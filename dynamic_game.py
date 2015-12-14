import random

from fwk.game.game import Game
from fwk.game.entity import GameEntity
from fwk.util.geometry import *

from fwk.ui.console import GAME_CONSOLE

import entities.supermassive_trash
import entities.teleport
import entities.trash

_INITIAL_CLEAR_SPACE = 900
_MAX_SPENT_FUEL = 150 # Before creating teleports
_TELEPORT_NEW_DENSITY = 0.15
_FAR_BORDERLINE = 4000
_NEAR_BORDERLINE = 2000

def not_in_square(sqCenter, sqRadius, point):
	return (point[0] < sqCenter[0] - sqRadius) \
		or (point[0] > sqCenter[0] + sqRadius) \
		or (point[1] < sqCenter[1] - sqRadius) \
		or (point[1] > sqCenter[1] + sqRadius)

class DynamicGame(Game):
	events = [
		'teleport-player',
		'hitBig'
	]

	def __init__(self,level_data):
		Game.__init__(self)
		self._generation = level_data['generation']

		self.initialGenerate()
		self._spent_fuel = 0

	def initialGenerate(self):
		self._generate(_INITIAL_CLEAR_SPACE, _FAR_BORDERLINE)
		self._prev_pp = (0,0)

	def periodicGenerate(self):
		self._killFar(_NEAR_BORDERLINE)
		self._generate(_NEAR_BORDERLINE, _FAR_BORDERLINE)
		self._prev_pp = self.player_pos

	def update(self, dt):
		if not_in_square(self._prev_pp, _NEAR_BORDERLINE, self.player_pos):
			self.periodicGenerate()

	@property
	def player_pos(self):
		return getattr(self.getEntityById('player'), 'position', (0,0))

	def onFuelSpent(self, amount):
		self._spent_fuel += amount
		if self._spent_fuel >= _MAX_SPENT_FUEL:
			self._generation['teleport-entity']['density'] = _TELEPORT_NEW_DENSITY

	def _generate(self, minDistance, maxDistance):
		playerPos = self.player_pos
		pmax = playerPos[0] + maxDistance, playerPos[1] + maxDistance
		pmin = playerPos[0] - maxDistance, playerPos[1] - maxDistance

		for cls, params in self._generation.items():
			clz = GameEntity.getClass(cls)
			amount = int(params['density'] * maxDistance * maxDistance / (1024*1024))
			for _ in range(amount):
				pos = random.uniform(pmin[0], pmax[0]), random.uniform(pmin[1], pmax[1])
				if not_in_square(playerPos, minDistance, pos):
					ent = clz()
					self.addEntity(ent)
					self.setEntityTags(ent, 'dynamic')
					ent.position = pos

	def _killFar(self, minDistance):
		playerPos = self.player_pos
		dynamic = self.getEntitiesByTag('dynamic')

		for ent in dynamic:
			if not_in_square(playerPos, minDistance, ent.position):
				ent.destroy()
