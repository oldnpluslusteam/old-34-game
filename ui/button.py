__author__ = 'moardm'

from fwk.ui.layers.guitextitem import GUITextItem


class Button(GUITextItem):

    def init(self, onclick, *args, **kwargs):
        self.on('ui:click', onclick)