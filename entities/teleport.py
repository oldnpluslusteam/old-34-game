from fwk.game.entity import GameEntity
from entities.physical import BigEntity
from fwk.ui.console import GAME_CONSOLE

@GameEntity.defineClass("teleport-entity")
class Teleport(GameEntity, BigEntity, GameEntity.mixin.Sprite):
	def spawn(self):
		self.sprite = 'rc/img/teleport.png'
		self.spriteAnchor = 'center'
		self.angularVelocity = 300
		self.radius = 128
		targetScale = float(self.radius*2)/self.sprite.width
		self.scale = targetScale

	def hitWith(self, smallEntity):
		if smallEntity == self.game.getEntityById('player'):
			self.game.trigger('teleport-player')

