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
from entities import meteorite, spaceship, supermassive_meteorite, trash, supermassive_trash, teleport

from fwk.util.all import *

from ui.progress_bar import ProgressBar
from ui.dynamic_bg import DynamicBG

def level2_data():
	return {
		'generation': {
			'supermassive-trash-entity': {
				'density': 1.0 # Things per 1024x1024 units
			},
			'trash-entity': {
				'density': 5.0
			},
			'teleport-entity': {
				'density': 0.0
			}
		},
		'next_data': None,
		'title': 'Level# 3'
	}

def level1_data():
	return {
		'generation': {
			'supermassive-trash-entity': {
				'density': 0.5 # Things per 1024x1024 units
			},
			'trash-entity': {
				'density': 10.0
			},
			'teleport-entity': {
				'density': 0.0
			}
		},
		'next_data': level2_data,
		'title': 'Level# 2'
	}

def level0_data():
	return {
		'generation': {
			'supermassive-trash-entity': {
				'density': 0.2 # Things per 1024x1024 units
			},
			'trash-entity': {
				'density': 20.0
			},
			'teleport-entity': {
				'density': 0.0
			}
		},
		'next_data': level1_data,
		'title': 'Level# 1'
	}

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
		self._camera.scale = 0.2

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

@Screen.ScreenClass('STARTUP')
class StartupScreen(Screen):
	def init(self, *args, **kwargs):
		self.next = Screen.new('GAME')

@Screen.ScreenClass('GAME')
class GameScreen(Screen):
	def init(self,level_data=level0_data,*args,**kwargs):
		self._ld = level_data()
		GAME_CONSOLE.write('Next level: ', self._ld['title'], '!')

		game = DynamicGame(level_data=self._ld)
		game.on('teleport-player', self.onNextLevel)
		game.loadFromJSON('rc/lvl/level0.json')

		self.pushLayerFront(DynamicBG(game.getEntityById('player')))
		self.pushLayerFront(GameLayer(game=game,camera=Camera()))
		self.pushLayerFront(ProgressBar(grow_origin='top-left',
			expression=lambda: game.getEntityById('player').fuel / 100.0,
			layout=ProgressBar.LEFT_LAYOUT,player=game.getEntityById('player')))

	def onNextLevel(self):
		if self._ld['next_data'] is not None:
			self.next = GameScreen(self._ld['next_data'])
		else:
			GAME_CONSOLE.write('End!')
			self.next = Screen.new('END')


	def on_key_press(self,key,mod):
		pass#GAME_CONSOLE.write('SSC:Key down:',KEY.symbol_string(key),'(',key,') [+',KEY.modifiers_string(mod),']')

@Screen.ScreenClass('END')
class EndScreen(Screen):
	pass
