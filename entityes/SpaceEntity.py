from fwk.game.entity import GameEntity


@GameEntity.defineClass("meteorite-entity")
class StandardSpaceEntity:

    def generateVelocityAndAngle(self, angle = {'start':0, 'end':0}, velocity = {'start':0, 'end':0}):
        pass # handle start angle and velocity