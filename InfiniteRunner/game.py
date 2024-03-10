from enum import Enum
import sys
import time
from random import random
from typing import List
import pygame as pg
from pygame import Rect, Vector2, mixer, image, transform
import pymunk
import pymunk.pygame_util
from effects.particle_system import SnowFallEffect

import settings
from entities.player import Player
from ui_panels.game_main_menu import GameMainMenu
from ui_panels.game_over_menu import GameOverMenu
from ui_panels.game_paused_menu import GamePausedMenu
from ui_panels.game_settings_menu import GameSettingsMenu
from renderer import Renderer
from utilities.colors import *
from entities.rectangle import Rectangle


class Game:
    class GameState(Enum):
        MAIN_MENU = 0,
        SETTINGS_MENU = 1,
        GAMEPLAY = 2,
        GAMEOVER = 3

    def __init__(self, renderer: Renderer):
        self.__renderer = renderer
        self.__display_surface = renderer.surface
        self.__is_paused = False
        self.__game_state = self.GameState.MAIN_MENU
        self.__delta_time = 0
        self.__score = 0
        self.__player_size = Vector2(40, 60)
        self.__player_spawn_pos = Vector2(
            100, 60 + 400)
        self.__start_platform_size = Vector2(250, 40)
        self.__platform_base_gap = 150
        self.__platform_base_size = 150
        self.__platform_gap_range = 150
        self.__platform_size_range = 200
        self.__off_screen_platfrom_length = 100
        self.__platform_initial_speed = -400
        self.__max_platform_speed = -1000

        self.__platform_speed = self.__platform_initial_speed
        self.__platforms: List[Rectangle] = []
        self.__last_grounded_platform: Rectangle = None

        self.__previous_frame_time = time.time()
        self.__checkBeforeStart = False

        self.__space = pymunk.Space()
        self.__space.gravity = 0, -100

        self.__setUpWorld()
        self.__bg_image = image.load("assets/bg.png").convert_alpha()
        self.__transform_bg_image = transform.scale(self.__bg_image, (int(
            self.__renderer.screenSize().x), int(self.__renderer.screenSize().y)))
        self.__first_bg_x = 0
        self.__second_bg_x = self.__renderer.screenSize().x
        self.__main_menu = GameMainMenu(self, self.__renderer)
        self.__settings_menu = GameSettingsMenu(self, self.__renderer)
        self.__paused_menu = GamePausedMenu(self, self.__renderer)
        self.__game_over_menu = GameOverMenu(self, self.__renderer)

        mixer.music.load("assets/background_music.wav")
        # self.__collect_sound = mixer.Sound("assets/collect.wav")
        # self.__health_loss_sound = mixer.Sound("assets/health_loss.wav")
        # self.__gameover_sound = mixer.Sound("assets/gameover.wav")
        mixer.music.play(-1)
        self.setVolume(settings.VOLUME)
        self.__snowFall = SnowFallEffect()

    def __createRectangle(self, pos: Vector2, size, angle=0, color=BLUE, body_type=pymunk.Body.KINEMATIC):
        pos = pos - size / 2
        rectangle = Rectangle(Rect(pos, size), angle,
                              color=color, body_type=body_type)
        rectangle.shape.density = 1
        rectangle.shape.friction = 1
        rectangle.shape.filter = pymunk.ShapeFilter(1)

        self.__space.add(rectangle.body, rectangle.shape)

        return rectangle

    def __generateStartPlatform(self):
        rectangle = self.__createRectangle(
            Vector2(self.__start_platform_size.x / 2, 150), self.__start_platform_size, color=(255, 128, 128))
        rectangle.shape.filter = pymunk.ShapeFilter(categories=4, mask=9)
        self.__platforms.append(rectangle)

    def __generateNextPlatform(self):
        if len(self.__platforms) == 0:
            self.__generateStartPlatform()
            return

        last_platform: Rectangle = self.__platforms[-1]
        cur_pos = last_platform.position
        cur_size = last_platform.size

        size = Vector2(self.__platform_base_size + random() *
                       self.__platform_size_range, cur_size.y)
        pos = cur_pos + Vector2(cur_size.x / 2 +
                                self.__platform_base_gap + random() * self.__platform_gap_range, -60 + random() * 120) + Vector2(size.x / 2, 0)

        pos = Vector2(pos.x, min(max(size.y / 2 + 60, pos.y),
                                 self.__renderer.screenSize().y - 400))
        rectangle = self.__createRectangle(pos, size, color=WHITE)
        rectangle.shape.filter = pymunk.ShapeFilter(categories=4, mask=9)
        self.__platforms.append(rectangle)

    def __setUpPlayer(self):
        self.__player = Player(self, self.__space, self.__player_spawn_pos, self.__player_size,
                               (81, 161, 250))

    def __setUpWorld(self):
        self.__setUpPlayer()
        self.__generateStartPlatform()

        while self.__platforms[-1].position.x + self.__platforms[-1].size.x / 2 < self.__renderer.screenSize().x + self.__off_screen_platfrom_length:
            self.__generateNextPlatform()

    def __calculateDeltaTime(self):
        self.__delta_time = time.time() - self.__previous_frame_time
        self.__previous_frame_time = time.time()

    def __pause(self):
        self.__is_paused = True

    def __reset(self):
        self.__score = 0
        # self.__particle_systems = []

    def __gameOver(self):
        if self.__space.bodies.__contains__(self.__player.body):
            self.__space.remove(self.__player.body, self.__player.shape)

        for platform in self.__platforms:
            # if self.__space.bodies.__contains__(platform.body):
            self.__space.remove(platform.body, platform.shape)

        self.__platforms = []
        self.__game_state = self.GameState.GAMEOVER
        self.__player.reset()

    def __handleEvents(self, events):
        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_p:
                if self.__game_state == self.GameState.MAIN_MENU:
                    self.startGame()
                elif self.__game_state == self.GameState.GAMEPLAY:
                    if self.__is_paused:
                        self.resume()
                    else:
                        self.__pause()
                elif self.__game_state == self.GameState.GAMEOVER:
                    self.__reset()
                    self.startGame()

        if self.__game_state == self.GameState.MAIN_MENU:
            self.__main_menu.handleEvents(events)
        elif self.__game_state == self.GameState.GAMEPLAY:
            if self.__is_paused:
                self.__paused_menu.handleEvents(events)
        elif self.__game_state == self.GameState.GAMEOVER:
            self.__game_over_menu.handleEvents(events)
        elif self.__game_state == self.GameState.SETTINGS_MENU:
            self.__settings_menu.handleEvents(events)

    def __drawMainMenuScreen(self):
        self.__main_menu.show(self.__delta_time)

    def __drawSettingsMenuScreen(self):
        self.__settings_menu.show()

    def __drawGameplayScreen(self):
        # self.__draw_options = pymunk.pygame_util.DrawOptions(
        #     self.__renderer.surface)
        # self.__space.debug_draw(self.__draw_options)
        self.__renderer.renderText("Score : {0}".format(self.__score), Vector2(
            self.__renderer.screenSize().x/2, self.__renderer.screenSize().y - 20), 20, color=TEAL)
        if self.__is_paused:
            self.__paused_menu.show()

    def __drawGameoverScreen(self):
        self.__game_over_menu.show()

    def setVolume(self, value):
        value = max(0, min(value, 1))
        mixer.music.set_volume(value)

    def startGame(self):
        self.__game_state = self.GameState.GAMEPLAY
        self.__space.add(self.__player.body, self.__player.shape)

        self.__checkBeforeStart = True
        self.__platform_speed = 0.0
        self.__player.reset()

        if len(self.__platforms) == 0:
            self.__generateStartPlatform()
        while self.__platforms[-1].position.x + self.__platforms[-1].size.x / 2 < self.__renderer.screenSize().x + self.__off_screen_platfrom_length:
            self.__generateNextPlatform()

    def mainMenu(self):
        self.__gameOver()
        self.__game_state = self.GameState.MAIN_MENU
        self.__checkBeforeStart = False

    def returnToMainMenu(self):
        self.__game_state = self.GameState.MAIN_MENU

    def settingsMenu(self):
        self.__game_state = self.GameState.SETTINGS_MENU

    def resume(self):
        self.__is_paused = False

    def exit(self):
        sys.exit(0)

    def update(self, events):
        self.__calculateDeltaTime()
        self.__handleEvents(events)
        
        self.__snowFall.update(self.__delta_time)

        self.__display_surface.fill(MAXIMUM_BLUE)
        self.__display_surface.blit(
            self.__transform_bg_image, (self.__first_bg_x, 0))
        self.__display_surface.blit(
            self.__transform_bg_image, (self.__second_bg_x, 0))
        # self.__display_surface.blit(self.__bg_image, (0, 0))

        if not self.__is_paused:
            self.__space.step(self.__delta_time)
            self.__first_bg_x += 0.008 * self.__platform_speed
            self.__second_bg_x += 0.008 * self.__platform_speed
            if self.__first_bg_x < self.__renderer.screenSize().x * -1:
                self.__first_bg_x = self.__second_bg_x + self.__renderer.screenSize().x
            if self.__second_bg_x < self.__renderer.screenSize().x * -1:
                self.__second_bg_x = self.__first_bg_x + self.__renderer.screenSize().x

        self.__snowFall.draw(self.__renderer)
        
        if self.__game_state == self.GameState.MAIN_MENU:
            self.__drawMainMenuScreen()
        elif self.__game_state == self.GameState.SETTINGS_MENU:
            self.__drawSettingsMenuScreen()
        elif self.__game_state == self.GameState.GAMEPLAY:
            if not self.__is_paused:
                self.__player.update(self.__platforms, events,
                                     self.__delta_time, self.__renderer)
                grounded_platfrom = self.__player.groundedPlatform
                if self.__last_grounded_platform != grounded_platfrom and grounded_platfrom != None:
                    self.__score += 1
                    self.__last_grounded_platform = grounded_platfrom
            for platform in self.__platforms:
                platform.draw(self.__renderer)
            
            self.__player.draw(self.__renderer)
            self.__drawGameplayScreen()
            if self.__checkBeforeStart:
                if self.__player.isGrounded:
                    self.__checkBeforeStart = False
                    self.__platform_speed = self.__platform_initial_speed
                    for plat in self.__platforms:
                        plat.body.velocity = [self.__platform_speed, 0]
            else:
                self.__platform_speed -= 10 * self.__delta_time
                self.__platform_speed = max(
                    self.__platform_speed, self.__max_platform_speed)
                for plat in self.__platforms:
                    plat.body.velocity = (self.__platform_speed, 0)
                while len(self.__platforms) > 1 and self.__platforms[0].size.x + self.__platforms[0].position.x < -10:
                    self.__space.remove(
                        self.__platforms[0].body, self.__platforms[0].shape)
                    self.__platforms.pop(0)

                while self.__platforms[-1].position.x + self.__platforms[-1].size.x / 2 < self.__renderer.screenSize().x + self.__off_screen_platfrom_length:
                    self.__generateNextPlatform()
        elif self.__game_state == self.GameState.GAMEOVER:
            self.__drawGameoverScreen()

        pg.display.update()

        if self.__player.position.y < -30:
            self.__gameOver()
