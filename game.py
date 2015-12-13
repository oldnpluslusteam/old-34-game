#!/usr/bin/python
# coding=UTF-8

from fwk.ui.screen import Screen
from fwk.ui.console import GAME_CONSOLE

from fwk.ui.layers.staticBg import StaticBackgroundLauer
from fwk.ui.layers.guiItem import GUIItemLayer
from fwk.ui.layers.guitextitem import GUITextItem
from fwk.ui.layers.gameLayer import GameLayer as GameLayer_
from fwk.ui.layers.texture9TileItem import *

from fwk.game.game import Game
from fwk.game.entity import GameEntity
from fwk.game.camera import Camera

import fwk.sound.static as ssound
import fwk.sound.music as music

from dynamic_game import DynamicGame
from entities import meteorite, spaceship, supermassive_meteorite, trash, supermassive_trash
from fwk.util.all import *

from ui.progress_bar import ProgressBar
from ui.dynamic_bg import DynamicBG
from ui.button import Button


class GameLayer(GameLayer_):
	'''
	Наследник игрового слоя.
	'''
	__KEYMAP = {
		KEY.RCTRL: {"action": "right_thruster"},
		KEY.LCTRL: {"action": "left_thruster"},
		KEY.ESCAPE: {"action": "pause"}
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
			if "action" in k:
				args = []
				if "args" in k:
					args += k["args"]
				fn = getattr(self, "press_" + k["action"])
				fn(args)

	def on_key_release(self, key, mod):
		if key in GameLayer.__KEYMAP:
			k = GameLayer.__KEYMAP[key]
			if "action" in k:
				args = []
				if "args" in k:
					args += k["args"]
				fn = getattr(self, "release_" + k["action"])
				fn(args)

	def press_right_thruster(self, *args):
		self._player.set_right_thruster(True)

	def release_right_thruster(self, *args):
		self._player.set_right_thruster(False)

	def press_left_thruster(self, *args):
		self._player.set_left_thruster(True)

	def release_left_thruster(self, *args):
		self._player.set_left_thruster(False)

	def press_pause(self, *args):
		pass

	def release_pause(self, *args):
		self.next = PauseScreen()

	def on_mouse_press(self,x,y,b,mod):
		'''
		Управление с мыши.
		'''
		self._player.position = self._camera.unproject((x, y))

	def draw(self):
		GameLayer_.draw(self)
		tep = self._camera.project(self._game.getEntityById('player').position)

	def on_pause(self):
		self.next = PauseScreen()


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
										layout={'height': 40, 'width': 300, 'top': 20, 'left': 20},
										player=game.getEntityById('player'))
		self.pushLayerFront(fuel_progress_bar)
		self.pushLayerFront(GUITextItem(text="Fuel", fontSize=20, layout={'top': 20, 'width': 100, 'height': 20, 'left': 125}))

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


	def init(self):
		self.pushLayerFront(StaticBackgroundLauer('rc/img/kxk-stars-bg.png', mode='fill'))

		self.pushLayerFront(Button(
			layout={'width': 256, 'height': 50, 'top': 200},
			text="New Game",
			onclick=self.new_game))
		self.pushLayerFront(Button(
			layout={'width': 256, 'height': 50, 'top': 300},
			text="Continue",
			onclick=self.Button))
		self.pushLayerFront(GUIItemLayer(
			layout={'width': 256, 'height': 50, 'top': 400},
			text="Exit",
			onclick=self.exit_game))

	def new_game(self):
			self.next = StartupScreen()
	def continue_game(self):
			pass
	def exit_game(self):
			pass