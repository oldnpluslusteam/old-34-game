from fwk.ui.layer import Layer
from fwk.ui.layers.staticBg import StaticBackgroundLauer
from fwk.util.all import *
from pyglet import gl


class DynamicBG(StaticBackgroundLauer):
	def __init__(self, player, bg):
		StaticBackgroundLauer.__init__(self, bg, 'fill')
		self._player = player

	def draw(self):
		pp = self._player.position
		k = 0.2 / 1024.0
		gl.glMatrixMode(gl.GL_TEXTURE)
		gl.glPushMatrix()
		# gl.glTranslatef(.5,.5, 0)
		gl.glTranslatef(pp[0]*k, pp[1]*k, 0)
		gl.glRotatef(-self._player.rotation,0,0,1.0)
		gl.glTranslatef(-.5,-.5, 0)
		BlitTextureToRect(self.texture,self.texture_rect)
		gl.glPopMatrix()
		gl.glMatrixMode(gl.GL_MODELVIEW)
