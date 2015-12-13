from fwk.game.entity import GameEntity
from entities.physical import BigEntity
from fwk.ui.console import GAME_CONSOLE

@GameEntity.defineClass("teleport-entity")
class Teleport(GameEntity, BigEntity, GameEntity.mixin.Sprite):
	def spawn(self):
		self.sprite = 'rc/img/64x64fg.png'
		self.spriteAnchor = 'center'
		self.angularVelocity = 300

	def hitWith(self, smallEntity):
		if smallEntity == self.game.getEntityById('player'):
			GAME_CONSOLE.write('Player teleported')
			self.game.trigger('teleport-player')

