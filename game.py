#!/usr/bin/python
# coding=UTF-8
from pyglet.media import Player

from fwk.sound import static
from fwk.ui.screen import Screen
from fwk.ui.console import GAME_CONSOLE

from fwk.ui.layers.staticBg import StaticBackgroundLauer
from fwk.ui.layers.guiItem import GUIItemLayer
from fwk.ui.layers.guitextitem import GUITextItem as GUITextItem_
from fwk.ui.layers.gameLayer import GameLayer as GameLayer_
from fwk.ui.layers.texture9TileItem import *

from fwk.game.game import Game
from fwk.game.entity import GameEntity
from fwk.game.camera import Camera

import fwk.sound.static as ssound
import fwk.sound.music as music

from dynamic_game import DynamicGame

from entities import meteorite, spaceship, supermassive_meteorite, trash, supermassive_trash, teleport

from fwk.util.all import *

from ui.progress_bar import ProgressBar
from ui.dynamic_bg import DynamicBG
from ui.button import Button

GAME_CONSOLE.visible = False

class GUITextItem(GUITextItem_):
	def draw(self):
		self._label.draw()

def level2_data():
	return {
		'generation': {
			'supermassive-trash-entity': {
				'density': 0.5 # Things per 1024x1024 units
			},
			'trash-entity': {
				'density': 2.5
			},
			'teleport-entity': {
				'density': 0.0
			}
		},
		'next_data': None,
		'title': 'Level# 3',
		'bg': 'rc/img/kosmosbg_uroven_3.png'
	}

def level1_data():
	return {
		'generation': {
			'supermassive-trash-entity': {
				'density': 0.25 # Things per 1024x1024 units
			},
			'trash-entity': {
				'density': 5.0
			},
			'teleport-entity': {
				'density': 0.0
			}
		},
		'next_data': level2_data,
		'title': 'Level# 2',
		'bg': 'rc/img/kosmosbg_uroven_2.png'
	}

def level0_data():
	return {
		'generation': {
			'supermassive-trash-entity': {
				'density': 0.2 # Things per 1024x1024 units
			},
			'trash-entity': {
				'density': 10.0
			},
			'teleport-entity': {
				'density': 0.0
			}
		},
		'next_data': level1_data,
		'title': 'Level# 1',
		'bg': 'rc/img/kosmosbg.png'
	}

class GameLayer(GameLayer_):
	'''
	Наследник игрового слоя.
	'''

	background_player = 0

	__KEYMAP = {
		KEY.RCTRL: {"action": "right_thruster"},
		KEY.LCTRL: {"action": "left_thruster"},
		KEY.P: {"action": "pause"}
	}
	def init(self,*args,**kwargs):
		print "Inited"
		self._player = self._game.getEntityById('player')
		self._camera.setController(self._player)
		self._camera.scale = 0.35

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
		self.ignore('update')
		games_screen = self.screen
		games_screen.next = Screen.new("PAUSE")

@Screen.ScreenClass('GAME')
class GameScreen(Screen):
	def init(self,level_data=level0_data,*args,**kwargs):
		self._ld = level_data()
		GAME_CONSOLE.write('Next level: ', self._ld['title'], '!')

		game = DynamicGame(level_data=self._ld)
		game.on('teleport-player', self.onNextLevel)
		game.loadFromJSON('rc/lvl/level0.json')
		self.game = game
		self.game.on("hitBig", self.foo)

		music.Play('rc/snd/background.wav')

		self.pushLayerFront(DynamicBG(game.getEntityById('player'), self._ld['bg']))
		self.game_layer = GameLayer(game=game, camera=Camera())
		self.pushLayerFront(self.game_layer)

		fuel_progress_bar = ProgressBar(grow_origin='top-left',
										expression=lambda: game.getEntityById('player')._fuel / 100.0,
										layout={'height': 40, 'width': 300, 'top': 20, 'left': 20},
										player=game.getEntityById('player'))
		self.pushLayerFront(fuel_progress_bar)
		self.pushLayerFront(GUITextItem(text="Fuel", fontSize=20, layout={'top': 20, 'width': 100, 'height': 20, 'left': 125}))
		self.pushLayerFront(Button(
			onclick=self.pause,
			layout={'width': 256, 'height': 50, 'right': 20, 'top': 20},
			text="Pause <P>"))

	def foo(self):
		GAME_CONSOLE.write('your died!')
		self.next = Screen.new('DEATHSCREEN')

	def win(self):
		GAME_CONSOLE.write('you are won!')
		self.next = Screen.new('WIN')

	def onNextLevel(self):
		if self._ld['next_data'] is not None:
			self.next = GameScreen(self._ld['next_data'])
		else:
			self.win()

	def on_show(self):
		self.game_layer.listen("update")

	def on_key_press(self,key,mod):
		pass#GAME_CONSOLE.write('SSC:Key down:',KEY.symbol_string(key),'(',key,') [+',KEY.modifiers_string(mod),']')

	def pause(self, *args):
		self.game_layer.release_pause()

@Screen.ScreenClass('PAUSE')
class PauseScreen(Screen):
	def init(self):
		self.keep_prevous = True
		self.pushLayerFront(StaticBackgroundLauer('rc/img/kxk-stars-bg.png', mode='fill'))

		self.pushLayerFront(Button(
			onclick=self.continue_game,
			layout={'width': 256, 'height': 50, 'top': 200},
			text="Continue"))
		self.pushLayerFront(Button(
			onclick=self.new_game,
			layout={'width': 256, 'height': 50, 'top': 300},
			text="New Game"))
		self.pushLayerFront(Button(
			onclick=self.exit_game,
			layout={'width': 256, 'height': 50, 'top': 400},
			text="Exit"))

	def new_game(self, *args):
		self.next = Screen.new('GAME')

	def continue_game(self, *args):
		self.next = self._prevous
		self.next.trigger("show")

	def exit_game(self, *args):
		exit()

@Screen.ScreenClass('DEATHSCREEN')
class DeathScreen(Screen):
	def init(self):
		self.pushLayerFront(StaticBackgroundLauer('rc/img/1600x1200bg_2.png', mode='fill'))

		self.pushLayerFront(GUITextItem(
			layout={'width': 256, 'height': 50, 'top': 200},
			text="You have died"))
		self.pushLayerFront(Button(
			onclick=self.new_game,
			layout={'width': 256, 'height': 50, 'top': 300},
			text="Next time..."))

	def new_game(self, *args):
		self.next = Screen.new('STARTUP')

@Screen.ScreenClass('WIN')
class WinScreen(Screen):
	def init(self):
		self.pushLayerFront(StaticBackgroundLauer('rc/img/1600x1200bg.png', mode='fill'))

		self.pushLayerFront(GUITextItem(
			layout={'width': 256, 'height': 50, 'top': 200},
			text="You have won"))
		self.pushLayerFront(Button(
			onclick=self.new_game,
			layout={'width': 256, 'height': 50, 'top': 300},
			text="GOTCHA"))

	def new_game(self, *args):
		self.next = Screen.new('STARTUP')

@Screen.ScreenClass('STARTUP')
class StartupScreen(Screen):
	def init(self):
		self.pushLayerFront(StaticBackgroundLauer('rc/img/1600x1200bg_2.png', mode='fill'))

		self.pushLayerFront(Button(
			onclick=self.new_game,
			layout={'width': 256, 'height': 50, 'top': 300},
			text="New Game"))
		self.pushLayerFront(Button(
			onclick=self.exit_game,
			layout={'width': 256, 'height': 50, 'top': 400},
			text="Exit"))

	def new_game(self, *args):
		self.next = Screen.new('GAME')

	def exit_game(self, *args):
		exit()

	# def init(self, *args, **kwargs):
	# 	self.next = Screen.new('GAME')
