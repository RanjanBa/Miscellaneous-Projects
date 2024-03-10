import pygame as pg
from pygame import Rect, Vector2

import settings
from renderer import Renderer
from utilities.colors import GRAY, WHITE


class Button:
    def __init__(self, label: str, rect: Rect, normal_color=WHITE, hover_color=(255, 237, 230), clicked_color=(235, 173, 221), disabled_color=GRAY) -> None:
        self.__y_offset = 0.0
        self.__y_max_offset = 3.0
        self.__width_offset = 0.0
        self.__width_max_offset = 10.0
        self.__label = label
        self.__rect = rect
        self.__normal_color = normal_color
        self.__clicked_color = clicked_color
        self.__hover_color = hover_color
        self.__disabled_color = disabled_color
        self.__is_clicked = False
        self.__is_hovered = False
        self.__click_events = []
        self.enabled = True
        self.interactable = True

    def addEvent(self, callback):
        self.__click_events.append(callback)

    def removeEvent(self, callback):
        self.__click_events.remove(callback)

    @property
    def rect(self) -> Rect:
        return self.__rect

    def handleEvents(self, events):
        mouse_pos = Vector2(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
        mouse_pos.y = settings.SCREEN_SIZE.y - mouse_pos.y
        if self.interactable:
            for event in events:
                if self.__rect.collidepoint(mouse_pos):
                    self.__is_hovered = True
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        self.__is_clicked = True
                        for e in self.__click_events:
                            e()
                    if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                        self.__is_clicked = False
                else:
                    self.__is_hovered = False
                    self.__is_clicked = False

    def show(self, renderer: Renderer):
        if self.enabled:
            color = self.__normal_color
            if self.interactable:
                if self.__is_clicked:
                    color = self.__clicked_color
                elif self.__is_hovered:
                    color = self.__hover_color
            else:
                color = self.__disabled_color

            if self.__is_hovered:
                self.__y_offset = min(
                    self.__y_offset + 0.5, self.__y_max_offset)
                self.__width_offset = min(
                    self.__width_offset + 0.5, self.__width_max_offset)
            else:
                self.__y_offset = max(0, self.__y_offset - 0.5)
                self.__width_offset = max(0, self.__width_offset - 0.5)

            r = Rect(Vector2(self.__rect.topleft[0] - self.__width_offset // 2, self.__rect.topleft[1] + self.__y_offset), Vector2(self.__rect.width + self.__width_offset, self.__rect.height))
            renderer.renderRect(r, color, border_radius=3)
            renderer.renderText(self.__label, r.center, 18, color=(179, 131, 27))
