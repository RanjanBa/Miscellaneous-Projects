from pygame import Rect, Vector2
from .menu_screen import MenuScreen
from ui_widgets.button import Button
from renderer import Renderer
from settings import BUTTON_SIZE


class GameOverMenu(MenuScreen):
    def __init__(self, game, renderer: Renderer):
        super().__init__(game, "GAME OVER", renderer)
        self.__btn_width = BUTTON_SIZE.x
        self.__btn_height = BUTTON_SIZE.y
        self.__play_again_btn = Button("Play Again", Rect(renderer.screenSize()/2 - Vector2(
            self.__btn_width / 2, 60), Vector2(self.__btn_width, self.__btn_height)))
        self.__main_menu_btn = Button("Main Menu", Rect(renderer.screenSize()/2 - Vector2(
            self.__btn_width / 2, 60 + self.__btn_height + 10), Vector2(self.__btn_width, self.__btn_height)))

        self.__play_again_btn.addEvent(lambda: game.startGame())
        self.__main_menu_btn.addEvent(lambda: game.mainMenu())
        self.__btns = [self.__play_again_btn, self.__main_menu_btn]
        self._instructions.append("Press key 'p' to play again")

    def handleEvents(self, events):
        for btn in self.__btns:
            btn.handleEvents(events)

    def show(self):
        super().show()
        for btn in self.__btns:
            btn.show(self._renderer)
