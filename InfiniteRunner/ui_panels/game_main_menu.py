from pygame import Vector2, Rect
from .menu_screen import MenuScreen

from ui_widgets.button import Button
from renderer import Renderer
from settings import BUTTON_SIZE, TITLE


class GameMainMenu(MenuScreen):
    def __init__(self, game, renderer: Renderer):
        super().__init__(game, TITLE, renderer)
        self.__time_passed = 0.0
        self.__btn_width = BUTTON_SIZE.x
        self.__btn_height = BUTTON_SIZE.y
        self.__space_between_btn = 10

        self.__is_animation_completed = False
        self.__speed = 2
        self.__start_left_pos = 20
        self.__end_left_pos = renderer.screenSize().x // 2 - self.__btn_width // 2

        top_left = Vector2(self.__end_left_pos -
                           self.__start_left_pos, renderer.screenSize().y // 2 - 60)
        self.__play_button = Button("Play", Rect(
            top_left, Vector2(self.__btn_width, self.__btn_height)))

        top_left.y -= self.__space_between_btn + self.__btn_height
        self.__settings_button = Button("Settings", Rect(
            top_left, Vector2(self.__btn_width, self.__btn_height)))

        top_left.y -= self.__space_between_btn + self.__btn_height
        self.__exit_button = Button("Exit", Rect(
            top_left, Vector2(self.__btn_width, self.__btn_height)))
        

        self.__delay_in_animation = 0.20
        self.__btns = [self.__play_button,
                       self.__settings_button, self.__exit_button]

        self.__play_button.addEvent(lambda: game.startGame())
        self.__settings_button.addEvent(lambda: game.settingsMenu())
        self.__exit_button.addEvent(lambda: game.exit())

        self._instructions.append("Press key 'p' to play")
        self._instructions.append("Press key 'esc' to exit")

    def handleEvents(self, events):
        for btn in self.__btns:
            btn.handleEvents(events)

    def show(self, delta_time):
        super().show()

        if not self.__is_animation_completed:
            for idx in range(len(self.__btns)):
                if self.__time_passed > idx * self.__delay_in_animation:
                    x_pos = min(
                        self.__btns[idx].rect.topleft[0] + self.__speed, self.__end_left_pos)
                    self.__btns[idx].rect.topleft = (
                        x_pos, self.__btns[idx].rect.topleft[1])

        for btn in self.__btns:
            btn.show(self._renderer)

        self.__time_passed += delta_time

        completed = True
        for btn in self.__btns:
            if btn.rect.topleft[0] < self.__end_left_pos:
                completed = False
                break

        self.__is_animation_completed = completed
