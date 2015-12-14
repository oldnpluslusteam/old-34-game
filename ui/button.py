__author__ = 'moardm'

from fwk.ui.layers.guiItem import GUIItemLayer
from fwk.util.graphics import LoadTexture
from fwk.ui.layers.texture9TileItem import _9Tiles
from fwk.util.all import *

class Button(GUIItemLayer):

	def init(self, onclick, img, layout, *args, **kwargs):
		self.on('ui:click', onclick)
		self.img = LoadTexture(img)

	def draw(self):
		BlitTextureToRect(self.img, self.rect)
		DrawWireframeRect(self.rect)
