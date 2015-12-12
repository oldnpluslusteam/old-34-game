from fwk.game.entity import GameEntity


@GameEntity.defineClass("meteorite-entity")
class Meteorite(GameEntity, GameEntity.mixin.Sprite, GameEntity.mixin.CameraTarget, GameEntity.mixin.Movement):

    def spawn(self):
        pass
