from fwk.game.game import Game
from fwk.util.geometry import distance

_MAX_TRASH = 20
_MAX_SUPERMASS_TRASH = 5
_MAX_METEORITE = 20
_MAX_SUPERMASS_METEORITE = 5


class DynamicGame(Game):

    _delay = 0.5
    _startRadius = 100
    _radius = 1000

    

    def __init__(self):
        Game.__init__(self)
        self.game.scheduleAfter(self._delay,self.check)

    def check(self):
        distance()
        self.generate()
        pass

    def generate(self, radius):
        pass