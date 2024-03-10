from pygame import Rect, Vector2
from pygame.constants import NOFRAME

import settings

from renderer import Renderer
from ui_widgets.dropdown import Dropdown
from utilities.colors import YELLOW
from .menu_screen import MenuScreen
from ui_widgets.button import Button
from ui_widgets.slider import Slider

class GameSettingsMenu(MenuScreen):
    def __init__(self, game, renderer: Renderer):
        super().__init__(game, "Settings", renderer)

        self.__slider_width = 300
        self.__slider_height = 20
        self.__dropdown_width = 150
        self.__dropdown_height = 35
        self.__btn_width = settings.BUTTON_SIZE.x
        self.__btn_height = settings.BUTTON_SIZE.y

        self.__old_selected_screen_size_index = 0
        for idx in range(len(settings.SCREEN_SIZES)):
            if settings.SCREEN_SIZES[idx][0] == settings.SCREEN_SIZE.x and settings.SCREEN_SIZES[idx][1] == settings.SCREEN_SIZE.y:
                self.__old_selected_screen_size_index = idx
                break

        pos = renderer.screenSize() / 2
        self.__slider_label_pos = pos - Vector2(0, 40)

        y_pos = self.__slider_label_pos.y - 40
        volume_slider_rect = Rect(Vector2(
            pos.x - self.__slider_width / 2, y_pos), Vector2(self.__slider_width, self.__slider_height))
        self.__volume_slider = Slider(volume_slider_rect, value=settings.VOLUME)

        y_pos -= (self.__slider_height + self.__dropdown_height)
        options_dropdown_rect = Rect(Vector2(
            pos.x - self.__dropdown_width / 2, y_pos), Vector2(self.__dropdown_width, self.__dropdown_height))

        dropdown_options = []
        for scree_size in settings.SCREEN_SIZES:
            dropdown_options.append(
                str(scree_size[0]) + "x" + str(scree_size[1]))
        self.__screen_options_dropdown = Dropdown(
            options_dropdown_rect, dropdown_options, default_index=self.__old_selected_screen_size_index)

        y_pos -= (self.__dropdown_height + 10)
        self.__save_settings_btn = Button("Save", Rect(Vector2(pos.x - self.__btn_width / 2, y_pos), Vector2(self.__btn_width, self.__btn_height)))

        y_pos -= (self.__btn_height + 10)
        self.__back_btn = Button("Back", Rect(Vector2(pos.x - self.__btn_width / 2,
                                                      y_pos), Vector2(self.__btn_width, self.__btn_height)))
        
        self.__volume_slider.addOnValueChanedListener(
            lambda x: game.setVolume(x))
        
        def applyChange():
            if self.__old_selected_screen_size_index != self.__screen_options_dropdown.selected_index or self.__volume_slider.value != settings.VOLUME:
                self.__old_selected_screen_size_index = self.__screen_options_dropdown.selected_index
                settings.save_data(Vector2(settings.SCREEN_SIZES[self.__screen_options_dropdown.selected_index]), self.__volume_slider.value)

        self.__save_settings_btn.addEvent(applyChange)
        
        def backBtn():
            game.returnToMainMenu()
            self.__screen_options_dropdown.selected_index = self.__old_selected_screen_size_index
        
        self.__back_btn.addEvent(backBtn)

    def handleEvents(self, events):
        self.__screen_options_dropdown.handleEvents(events)
        if not self.__screen_options_dropdown.isInputHandled:
            self.__volume_slider.handleEvents(events)
            self.__save_settings_btn.handleEvents(events)
            self.__back_btn.handleEvents(events)

    def show(self):
        super().show()
        self._renderer.renderText(
            "Volume", self.__slider_label_pos, 20, YELLOW)
        self.__volume_slider.show(self._renderer)
        self.__save_settings_btn.show(self._renderer)
        self.__back_btn.show(self._renderer)
        self.__screen_options_dropdown.show(self._renderer)
