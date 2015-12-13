from pyglet import gl

from fwk.ui.layers.guiItem import GUIItemLayer
from fwk.ui.layers.texture9TileItem import _9Tiles
from fwk.util.graphics import LoadTexture
from fwk.util.rect import Rect


class ProgressBar(GUIItemLayer):
	STANDARD_LAYOUT  = {'height': 30, 'width': 100}
	def init(self,grow_origin,expression,*args,**kwargs):
		self._expression = expression
		self._grow_origin = grow_origin
		self.back = _9Tiles(LoadTexture('rc/img/ui-frames.png'),Rect(left=0,bottom=0,width=12,height=12))
		self.front = _9Tiles(LoadTexture('rc/img/ui-frames.png'),Rect(left=12,bottom=0,width=12,height=12))
		self._expRes = 65595
		self.on_layout_updated()

	def draw(self):
		self.back.draw(self.rect)
		k = self._expression()
		if self._inrect is None or k != self._expRes:
			self._inrect = self.rect.clone().inset(5).scale(scaleX=k,scaleY=1,origin=self._grow_origin)
			self._expRes = k

		if k > 0:
			if k < 0.4:
				gl.glColor3ub(255,0,0)
			elif k < 0.7:
				gl.glColor3ub(255,255,0)
			else:
				gl.glColor3ub(0,255,0)
			self.front.draw(self._inrect)
			gl.glColor3ub(255,255,255)

	def on_layout_updated(self):
		self._inrect = None