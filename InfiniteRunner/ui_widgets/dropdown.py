from typing import List
import pygame as pg

from pygame import Rect, Vector2

import settings
from renderer import Renderer
from utilities.colors import WHITE


class Dropdown:
    def __init__(self, rect: Rect, options: List[str], default_index=0, bg_color=WHITE, option_color=(239, 233, 231), option_hover_color=(229, 198, 135)):
        self.selected_index = default_index
        self.__options = options
        self.__bg_color = bg_color
        self.__option_color = option_color
        self.__option_hover_color = option_hover_color
        self.__rect = rect
        self.__hovered_index = -1
        self.__is_showing_options = False
        self.__is_input_handled = False
        self.__rect_options: List[Rect] = []

        pos = Vector2(self.__rect.topleft) - Vector2(0, self.__rect.height)
        for option in options:
            r = Rect(pos, Vector2(self.__rect.width, self.__rect.height))
            self.__rect_options.append(r)
            pos.y -= self.__rect.height

    @property
    def isInputHandled(self):
        return self.__is_input_handled

    def handleEvents(self, events):
        mouse_pos = pg.mouse.get_pos()
        mouse_pos = Vector2(mouse_pos[0], settings.SCREEN_SIZE.y - mouse_pos[1])

        self.__is_input_handled = False
        self.__hovered_index = -1
        if self.__rect.collidepoint(mouse_pos):
            self.__is_input_handled = True

        if self.__is_showing_options:
            for idx in range(len(self.__rect_options)):
                r = self.__rect_options[idx]
                if r.collidepoint(mouse_pos):
                    self.__hovered_index = idx
                    self.__is_input_handled = True

        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if not self.__is_showing_options:
                    if self.__rect.collidepoint(mouse_pos):
                        self.__is_showing_options = True
                else:
                    for idx in range(len(self.__rect_options)):
                        r = self.__rect_options[idx]
                        if r.collidepoint(mouse_pos):
                            self.selected_index = idx
                    self.__is_showing_options = False

    def show(self, renderer: Renderer):
        h = self.__rect.height
        if self.__is_showing_options:
            for r in self.__rect_options:
                h += r.height

        r = Rect(self.__rect.left, self.__rect.top - h +
                 self.__rect.height, self.__rect.width, h)
        renderer.renderRect(r, self.__bg_color, border_radius=4)
        renderer.renderText(
            self.__options[self.selected_index], Vector2(self.__rect.center), font_size=18, color=(179, 131, 27))

        if self.__is_showing_options:
            for idx in range(len(self.__rect_options)):
                r = self.__rect_options[idx]
                color = self.__option_color
                if idx == self.__hovered_index:
                    color = self.__option_hover_color

                if idx == len(self.__rect_options) - 1:
                    renderer.renderRect(r, color, border_radii=(4, 4, 0, 0))
                else:
                    renderer.renderRect(r, color)
                renderer.renderText(self.__options[idx], Vector2(
                    r.center), font_size=18, color=(179, 131, 27))
