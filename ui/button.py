__author__ = 'moardm'

from fwk.ui.layers.guiItem import GUIItemLayer


class Button(GUIItemLayer):

    def init(self, layout, onclick, **kwargs):
        self.on_click = onclick