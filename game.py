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
from entities import meteorite, spaceship, supermassive_meteorite

from fwk.util.all import *

# @GameEntity.defineClass('test-entity')
# class TestEntity(GameEntity,GameEntity.mixin.Animation,GameEntity.mixin.Movement):
# 	def spawn(self):
# 		self.angularVelocity = 100
# 		self.i = 0
# 		self.think()
#
# 	def think(self):
# 		if self.i > 10:
# 			return self.destroy()
# 		self.game.scheduleAfter(1.0,self.think)
# 		self.position = (self.i*10 % 40,-self.i*20 % 50)
# 		self.velocity = (self.i*2353 % 100 - 50,-self.i*5423 % 110 - 55)
# 		self.i += 1
#
# @GameEntity.defineClass('test-player')
# class TestPlayer(GameEntity,GameEntity.mixin.Sprite,GameEntity.mixin.CameraTarget,GameEntity.mixin.Movement):
# 	pass

# @GameEntity.defineClass('static-entity')
# class StaticEntity(GameEntity,GameEntity.mixin.Sprite):
# 	'''
# 	Просто статическая спрайтовая сущность с нестандартным z-индексом.
# 	'''
# 	z_index = -1
from ui.progress_bar import ProgressBar


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
		DrawWireframeRect(Rect(left=tep[0],bottom=tep[1],width=100,height=100))


@Screen.ScreenClass('STARTUP')
class StartupScreen(Screen):

	def init(self,*args,**kwargs):

		# self.pushLayerFront(StaticBackgroundLauer('rc/img/256x256bg.png','fill'))

		game = Game()

		game.loadFromJSON('rc/lvl/level0.json')

		self.pushLayerFront(GameLayer(game=game,camera=Camera()))

		self.pushLayerFront(ProgressBar(grow_origin='top-left',
			expression=lambda: game.getEntityById('player').fuel / 100.0,
			layout=ProgressBar.LEFT_LAYOUT,player=game.getEntityById('player')))

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
