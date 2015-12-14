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

import math

GAME_CONSOLE.visible = False

class GUITextItem(GUITextItem_):
	def draw(self):
		self._label.draw()

def level2_data():
	return {
		'generation': {
			'supermassive-trash-entity': {
				'density': 0.45 # Things per 1024x1024 units
			},
			'trash-entity': {
				'density': 6.0
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
				'density': 0.3 # Things per 1024x1024 units
			},
			'trash-entity': {
				'density': 7.0
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
				'density': 0.25 # Things per 1024x1024 units
			},
			'trash-entity': {
				'density': 8.0
			},
			'teleport-entity': {
				'density': 0.0
			}
		},
		'next_data': None,
		'title': 'Level# 1',
		'bg': 'rc/img/kosmosbg.png'
	}

class GameLayer(GameLayer_):
	'''
	Наследник игрового слоя.
	'''

	_NORMAL_DIAGONAL = 1000.0
	_NORMAL_ZOOM = 0.35
	_MIN_ZOOM = 0.20
	_MAX_ZOOM = 2.0

	__KEYMAP = {
		KEY.X: {"action": "right_thruster"},
		KEY.Z: {"action": "left_thruster"},
		KEY.P: {"action": "pause"}
	}
	def init(self,*args,**kwargs):
		print "Inited"
		self._player = self._game.getEntityById('player')
		self._camera.setController(self._player)
		self._camera.scale = 0.35
		GAME_CONSOLE.write('INI GL')

	def on_add_to_screen(self, screen):
		self.subscribe(self.screen, 'vp:resize')
		self.listen('vp:resize')

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

	def on_viewport_resize(self, oldWidth, oldHeight):
		diag = math.sqrt(self.width**2 + self.height**2)
		z = self._NORMAL_ZOOM * (diag / self._NORMAL_DIAGONAL)
		z = min(self._MAX_ZOOM, max(self._MIN_ZOOM, z))
		self._camera.scale = z

@Screen.ScreenClass('GAME')
class GameScreen(Screen):
	def init(self,level_data=level0_data,*args,**kwargs):
		music.Play('rc/snd/background.wav')
		self._ld = level_data()
		GAME_CONSOLE.write('Next level: ', self._ld['title'], '!')

		if level_data == level0_data:
			spaceship.Spaceship._fuel = 100

		game = DynamicGame(level_data=self._ld)
		game.on('teleport-player', self.onNextLevel)
		game.loadFromJSON('rc/lvl/level0.json')
		self.game = game
		self.game.on("hitBig", self.foo)

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
			layout={'width': 256, 'height': 64, 'right': 20, 'top': 20},
			img="rc/img/256x64_menu_btn.png"))

	def foo(self):
		GAME_CONSOLE.write('your died!')
		self.next = Screen.new('DEATHSCREEN')
		self.endOfGame()

	def win(self):
		GAME_CONSOLE.write('you are won!')
		self.next = Screen.new('WIN')
		self.endOfGame()

	def endOfGame(self):
		pass

	def onNextLevel(self):
		if self._ld['next_data'] is not None:
			self.next = GameScreen(self._ld['next_data'])
		else:
			self.win()

	def on_show(self):
		self.game_layer.listen("update")
		# self.background_player.play()

	def hide(self,hide=True):
		pass# self.background_player.pause()

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
			layout={'width': 256, 'height': 64, 'top': 200},
			img="rc/img/256x64_continue_btn.png"))
		self.pushLayerFront(Button(
			onclick=self.new_game,
			layout={'width': 256, 'height': 64, 'top': 300},
			img="rc/img/256x64_new_game_btn.png"))
		self.pushLayerFront(Button(
			onclick=self.menu,
			layout={'width': 256, 'height': 64, 'top': 400},
			img="rc/img/256x64_menu_btn.png"))

	def new_game(self, *args):
		self.next = Screen.new('GAME')

	def continue_game(self, *args):
		self.next = self._prevous
		self.next.trigger("show")

	def menu(self, *args):
		self.next = Screen.new('STARTUP')

@Screen.ScreenClass('DEATHSCREEN')
class DeathScreen(Screen):
	def init(self):
		self.pushLayerFront(StaticBackgroundLauer('rc/img/1600x1200bg_2.png', mode='fill'))

		self.pushLayerFront(GUITextItem(
			layout={'width': 256, 'height': 64, 'top': 200},
			text="You have died"))
		self.pushLayerFront(Button(
			onclick=self.new_game,
			layout={'width': 256, 'height': 64, 'top': 300},
			img="rc/img/256x64_new_game_btn.png"))

	def new_game(self, *args):
		self.next = Screen.new('STARTUP')

# @Screen.ScreenClass('STARTUP') # Unomment to show on startup (& comment other one)
@Screen.ScreenClass('WIN')
class WinScreen(Screen):
	def init(self):
		# music.Play('rc/snd/background.wav') # <------------------------------------------------------------------------- FINAL MUSIC
		self.schedule = Schedule()
		self.on('update', self.schedule.update)
		self.schedule.scheduleAfter(1, self.foo_00)
		self.pushLayerFront(StaticBackgroundLauer('rc/img/1600x1200bg.png', mode='scale'))

	def foo_00(self):
		self._titrbI = GUITextItem(
			layout={'width': 256, 'height': 64, 'top': 100},
			text="...what's happened?..")
		self.pushLayerFront(self._titrbI)
		self.schedule.scheduleAfter(8, self.foo_02)

	def foo_02(self):
		self._titrbI.text = 'THANK YOU for playing!'
		self.schedule.scheduleAfter(4, self.foo_02t)

	def foo_02t(self):
		self._titrbI.text = 'OpeNPP Team:'
		self.schedule.scheduleAfter(2, self.foo_031)

	def foo_031(self):
		self._titrbI.text = 'Dev leader: A. Bond'
		self.schedule.scheduleAfter(2, self.foo_032)

	def foo_032(self):
		self._titrbI.text = 'Code: A. Moiseenko'
		self.schedule.scheduleAfter(2, self.foo_033)

	def foo_033(self):
		self._titrbI.text = 'Code: A. Ovsyannikov'
		self.schedule.scheduleAfter(2, self.foo_034)

	def foo_034(self):
		self._titrbI.text = 'Code: D. Shatov'
		self.schedule.scheduleAfter(2, self.foo_04)

	def foo_04(self):
		self._titrbI.text = 'Art: S. Balashova'
		self.schedule.scheduleAfter(2, self.foo_05)

	def foo_05(self):
		self._titrbI.text = 'Art: Mara Sun'
		self.schedule.scheduleAfter(2, self.foo_06)

	def foo_06(self):
		self._titrbI.text = 'Music and sounds: D. Shatov'
		self.schedule.scheduleAfter(2, self.foo_06c)

	def foo_06c(self):
		self._titrbI.text = ''
		self.schedule.scheduleAfter(1, self.foo_07)

	def foo_07(self):
		self.pushLayerFront(StaticBackgroundLauer('rc/img/1600x1200bg_f2.png', mode='scale'))
		self.schedule.scheduleAfter(7, self.foo_09)

	def foo_09(self):
		self.pushLayerFront(StaticBackgroundLauer('rc/img/Kosmo4.png', mode='scale'))
		self.schedule.scheduleAfter(7, self.foo_10)

	def foo_10(self):
		self.pushLayerFront(Button(
			onclick=self.menu,
			layout={'width': 256, 'height': 64, 'top': 20},
			img="rc/img/256x64_menu_btn.png"))

	def menu(self, *args):
		self.next = Screen.new('STARTUP')

@Screen.ScreenClass('STARTUP')
class StartupScreen(Screen):

	def init(self):
		music.Play("rc/snd/menu.wav")
		self.pushLayerFront(StaticBackgroundLauer('rc/img/1600x1200bg_2.png', mode='fill'))

		self.pushLayerFront(Button(
			onclick=self.new_game,
			layout={'width': 256, 'height': 64, 'top': 200},
			img="rc/img/256x64_new_game_btn.png"))
		self.pushLayerFront(Button(
			onclick=self.tutorial,
			layout={'width': 256, 'height': 64, 'top': 300},
			img="rc/img/256x64_tutorial_btn.png"))
		self.pushLayerFront(Button(
			onclick=self.exit_game,
			layout={'width': 256, 'height': 64, 'top': 400},
			img="rc/img/256x64_exit_btn.png"))

	def new_game(self, *args):
		self.next = Screen.new('GAME')

	def exit_game(self, *args):
		exit()

	def tutorial(self, *args):
		self.next = Screen.new('TUTORIAL')

@Screen.ScreenClass('TUTORIAL')
class TutorialScreen(Screen):
	def init(self):
		# ТУТ КАРТИНКА С ТУТОРИАЛОМ
		self.pushLayerFront(StaticBackgroundLauer('rc/img/tutorial.png', mode='scale'))
		self.pushLayerFront(Button(
			onclick=self.menu,
			# left, right, top, bottom - отступы с краёв
			# width, height - ставить как у картинки
			layout={'width': 256, 'height': 64, 'bottom': 10, 'right': 20},
			img="rc/img/256x64_menu_btn.png"))

	def menu(self, *args):
		self.next = Screen.new('STARTUP')
