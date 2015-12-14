__author__ = 'moardm'

from fwk.ui.layers.guitextitem import GUITextItem
from fwk.util.graphics import LoadTexture
from fwk.ui.layers.texture9TileItem import _9Tiles
from fwk.util.rect import Rect

class Button(GUITextItem):

	def init(self, onclick, img, layout, *args, **kwargs):
		self.on('ui:click', onclick)
		self.img = _9Tiles(LoadTexture(img), Rect(left=0, bottom=0, width=layout['width'], height=layout['height']))
		self.on_layout_updated()

	def draw(self):
		self.img.draw(self.rect)

	def on_layout_updated(self):
		self._inrect = None