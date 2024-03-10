from pygame import Vector2, Rect
from pygame.sprite import RenderClear

from renderer import Renderer
from .menu_screen import MenuScreen
from ui_widgets.button import Button
from settings import BUTTON_SIZE


class GamePausedMenu(MenuScreen):
    def __init__(self, game, renderer: Renderer):
        super().__init__(game, "PAUSED", renderer)
        self.__btn_width = BUTTON_SIZE.x
        self.__btn_hieght = BUTTON_SIZE.y
        self.__resume_btn = Button("Resume", Rect(renderer.screenSize() / 2 - Vector2(
            self.__btn_width/2, 60), Vector2(self.__btn_width, self.__btn_hieght)))
        self.__resume_btn.addEvent(lambda: game.resume())
        self.__btns = [self.__resume_btn]
        self._instructions.append("Press key 'p' to resume")

    def handleEvents(self, events):
        for btn in self.__btns:
            btn.handleEvents(events)

    def show(self):
        super().show()
        for btn in self.__btns:
            btn.show(self._renderer)
