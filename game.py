#!/usr/bin/python
# coding=UTF-8

from fwk.ui.screen import Screen
from fwk.ui.layers.gameLayer import GameLayer as GameLayer_
from fwk.game.camera import Camera
from dynamic_game import DynamicGame
from fwk.util.all import *
from ui.progress_bar import ProgressBar
from ui.dynamic_bg import DynamicBG

class GameLayer(GameLayer_):
	'''
	Наследник игрового слоя.
	'''
	__KEYMAP = {
		KEY.RCTRL: {"action": "set_right_thruster"},
		KEY.LCTRL: {"action": "set_left_thruster"}
	}
	def init(self,*args,**kwargs):
		self._player = self._game.getEntityById('player')
		self._camera.setController(self._player)
		self._camera.scale = 0.4

	def on_key_press(self,key,mod):
		'''
		Здесь происходит управление с клавиатуры.
		'''
		if key in GameLayer.__KEYMAP:
			k = GameLayer.__KEYMAP[key]
			fn = getattr(self._player, k["action"])
			if fn is not None:
				fn(True)

	def on_key_release(self, key, mod):
		if key in GameLayer.__KEYMAP:
			k = GameLayer.__KEYMAP[key]
			fn = getattr(self._player, k["action"])
			if fn is not None:
				fn(False)


	def on_mouse_press(self,x,y,b,mod):
		'''
		Управление с мыши.
		'''
		self._player.position = self._camera.unproject((x, y))

	def draw(self):
		GameLayer_.draw(self)
		tep = self._camera.project(self._game.getEntityById('player').position)


@Screen.ScreenClass('STARTUP')
class StartupScreen(Screen):

	def init(self,*args,**kwargs):

		# self.pushLayerFront(StaticBackgroundLauer('rc/img/256x256bg.png','fill'))

		game = DynamicGame()

		game.loadFromJSON('rc/lvl/level0.json')

		self.pushLayerFront(DynamicBG(game.getEntityById('player')))

		self.pushLayerFront(GameLayer(game=game, camera=Camera()))

		fuel_progress_bar = ProgressBar(grow_origin='top-left',
										expression=lambda: game.getEntityById('player')._fuel / 100.0,
										layout=ProgressBar.STANDARD_LAYOUT,
										player=game.getEntityById('player'))

		self.pushLayerFront(fuel_progress_bar)

		# ssound.Preload('rc/snd/1.wav',['alias0'])
        #
		# musmap = {}
        #
		# for x in musmap.iteritems():
		# 	layer = GUITextItem(
		# 		layout={
		# 			'width':100,
		# 			'height':20,
		# 			'left':50,
		# 			'right':50,
		# 			'offset_y':70*x,
		# 			'padding':[20,10],
		# 			'force-size':False
		# 			},
		# 		text=musmap[x]);
		# 	layer.on('ui:click',(lambda x: lambda *a: music.Play(musmap[x],loop=True))(x))
		# 	self.pushLayerFront(layer)
        #
		# tile = _9Tiles(LoadTexture('rc/img/ui-frames.png'),Rect(left=0,bottom=0,width=12,height=12))
        #
		# self.pushLayerFront(GUI9TileItem(
		# 	tiles=tile,
		# 	layout = {
		# 		'left': 100,
		# 		'right': 100,
		# 		'top': 200,
		# 		'bottom': 200
		# 	}))
        #
		# GAME_CONSOLE.write('Startup screen created.')

	def on_key_press(self,key,mod):
		pass#GAME_CONSOLE.write('SSC:Key down:',KEY.symbol_string(key),'(',key,') [+',KEY.modifiers_string(mod),']')

@Screen.ScreenClass('PAUSE')
class PauseScreen(Screen):
	def init(self,*args,**kwargs):
		pass