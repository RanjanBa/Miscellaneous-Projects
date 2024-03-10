from abc import ABC, abstractmethod

from pygame import Vector2

from renderer import Renderer
from utilities.colors import GRAY, YELLOW


class MenuScreen(ABC):
    def __init__(self, game, screen_title, renderer: Renderer, title_color=YELLOW):
        self._game = game
        self._screen_title = screen_title
        self._title_color = title_color
        self._instructions = []
        self._renderer = renderer

    def titlePos(self) -> Vector2:
        return self._renderer.screenSize()/2.0

    @abstractmethod
    def handleEvents(self, events):
        pass

    def show(self):
        pos = self.titlePos()
        self._renderer.renderText(
            self._screen_title, pos, font_size=30, color=self._title_color)
        pos.y = 30
        for idx in range(len(self._instructions) - 1, -1, -1):
            self._renderer.renderText(
                self._instructions[idx], pos, font_size=20, color=GRAY)
            pos.y += 25
