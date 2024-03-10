import pygame as pg
from pygame import Rect, Vector2

import settings
from renderer import Renderer
from utilities.colors import GRAY, TEAL, WHITE


class Slider:
    def __init__(self, rect: Rect, value=0, inner_offset=2, handle_size=10, bg_color=WHITE, inner_color=GRAY, handle_color=TEAL):
        self.__value = value

        self.__rect = rect
        self.__inner_rect = Rect(Vector2(self.__rect.topleft) + Vector2(inner_offset, inner_offset),
                                 Vector2(self.__rect.width - 2 * inner_offset, self.__rect.height - 2 * inner_offset))

        self.__handle_rect = Rect(self.__inner_rect.topleft - Vector2(handle_size / 2, inner_offset + 4) + Vector2(self.__value * self.__inner_rect.width, 0),
                                  Vector2(handle_size, self.__rect.height + 8))

        self.__handle_size = handle_size
        self.__bg_color = bg_color
        self.__inner_color = inner_color
        self.__handle_color = handle_color
        self.__is_dragging = False
        self.__onValueChangedListeners = []

        mouse_pos = pg.mouse.get_pos()
        self.__last_frame_mouse_pos = Vector2(
            mouse_pos[0], settings.SCREEN_SIZE.y - mouse_pos[1])

    @property
    def value(self):
        return self.__value

    def setValue(self, value):
        self.__value = value

    def addOnValueChanedListener(self, callback):
        self.__onValueChangedListeners.append(callback)

    def removeOnValueChanedListener(self, callback):
        self.__onValueChangedListeners.remove(callback)

    def handleEvents(self, events):
        mouse_pos = pg.mouse.get_pos()
        mouse_pos = Vector2(
            mouse_pos[0], settings.SCREEN_SIZE.y - mouse_pos[1])

        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.__handle_rect.collidepoint(mouse_pos):
                    self.__is_dragging = True
                    self.__last_frame_mouse_pos = mouse_pos
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.__is_dragging = False

        if self.__is_dragging:
            old_value = self.__value
            delta_pos = mouse_pos - self.__last_frame_mouse_pos
            x_pos = self.__handle_rect.topleft[0] + delta_pos.x
            x_pos = max(
                x_pos, self.__inner_rect.topleft[0] - self.__handle_size / 2)
            x_pos = min(
                x_pos, self.__inner_rect.topright[0] - self.__handle_size / 2)
            self.__handle_rect.topleft = (x_pos, self.__handle_rect.topleft[1])
            self.__value = (self.__handle_rect.topleft[0] - (
                self.__inner_rect.topleft[0] - self.__handle_size / 2)) / self.__inner_rect.width

            if old_value != self.__value:
                for listener in self.__onValueChangedListeners:
                    listener(self.__value)

        self.__last_frame_mouse_pos = mouse_pos

    def show(self, renderer: Renderer):
        renderer.renderRect(self.__rect, color=self.__bg_color)
        renderer.renderRect(self.__inner_rect, color=self.__inner_color)
        renderer.renderRect(self.__handle_rect,
                            self.__handle_color, border_radius=2)
