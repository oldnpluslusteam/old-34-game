import random

from fwk.game.game import Game
from fwk.game.entity import GameEntity
from fwk.util.geometry import *

from fwk.ui.console import GAME_CONSOLE

import entities.supermassive_trash
import entities.trash

_INITIAL_CLEAR_SPACE = 256
_FAR_BORDERLINE = 1000
_NEAR_BORDERLINE = 800
_REGENERATE_INTERVAL = 5.0

_GENERATION_DISTRIBUTION = {
	'supermassive-trash-entity': {
		'density': 0.5 # Things per 1024x1024 units
	},
	'trash-entity': {
		'density': 10.0
	}
}

def not_in_square(sqCenter, sqRadius, point):
	return (point[0] < sqCenter[0] - sqRadius) \
		or (point[0] > sqCenter[0] + sqRadius) \
		or (point[1] < sqCenter[1] - sqRadius) \
		or (point[1] > sqCenter[1] + sqRadius)

class DynamicGame(Game):
	def __init__(self):
		Game.__init__(self)
		self.initialGenerate()

	def initialGenerate(self):
		self._generate(_INITIAL_CLEAR_SPACE, _FAR_BORDERLINE)
		self.scheduleAfter(_REGENERATE_INTERVAL, self.periodicGenerate)

	def periodicGenerate(self):
		self._killFar(_NEAR_BORDERLINE)
		self._generate(_NEAR_BORDERLINE, _FAR_BORDERLINE)
		self.scheduleAfter(_REGENERATE_INTERVAL, self.periodicGenerate)

	@property
	def player_pos(self):
		return getattr(self.getEntityById('player'), 'position', (0,0))

	def _generate(self, minDistance, maxDistance):
		playerPos = self.player_pos
		pmax = playerPos[0] + maxDistance, playerPos[1] + maxDistance
		pmin = playerPos[0] - maxDistance, playerPos[1] - maxDistance

		for cls, params in _GENERATION_DISTRIBUTION.items():
			clz = GameEntity.getClass(cls)
			amount = int(params['density'] * maxDistance * maxDistance / (1024*1024))
			GAME_CONSOLE.write('Amount of ', cls, ' is ', amount)
			for _ in range(amount):
				pos = random.uniform(pmin[0], pmax[0]), random.uniform(pmin[1], pmax[1])
				if not_in_square(playerPos, minDistance, pos):
					ent = clz()
					self.addEntity(ent)
					self.setEntityTags(ent, 'dynamic')
					ent.position = pos

		GAME_CONSOLE.write('Generate complete!')

	def _killFar(self, minDistance):
		playerPos = self.player_pos
		dynamic = self.getEntitiesByTag('dynamic')

		n = 0

		for ent in dynamic:
			if not_in_square(playerPos, minDistance, ent.position):
				ent.destroy()
				n += 1
		GAME_CONSOLE.write('killed ', n)
