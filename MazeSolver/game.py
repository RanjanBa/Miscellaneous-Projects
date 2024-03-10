from enum import Enum
import time
import math
from random import randint, random
import pygame as pg
from pygame import Vector2, mixer
from entitites.bomb import Bomb
from entitites.character import Character
from entitites.enemy import Enemy

from entitites.grid import Grid
from entitites.level_generator import levelGenerator
from entitites.particle_system import ParticleSystem
from entitites.player import Player
from entitites.world import World

from renderer import Renderer
from utilities.colors import *
from settings import GRID_SIZE, LINE_WIDTH, TITLE
from utilities.rect import Rect


class Game:
    class GameState(Enum):
        MENU = 0,
        GAMEPLAY = 1,
        GAMEOVER = 2

    def __init__(self, renderer: Renderer):
        self.__renderer = renderer
        self.__display_surface = renderer.surface
        self.__is_paused = False
        self.__game_state = self.GameState.MENU
        self.__delta_time = 0
        self.__previous_frame_time = time.time()

        self.__last_key_pressed_timer = 0
        self.__retain_key_pressed_duration = 0.5

        self.__desired_move_dir: Character.MoveDirection = Character.MoveDirection.NONE

        self.__world = World()

        self.__world.loadLevel("levels\level1.png")

        self.__player = Player(self.__world, self.__world.getPositionAtCoordinate(
            5, 8), 100.0, GRID_SIZE.x / 2 - 4)
        self.__player.target_cell = Vector2(0, 23)

        self.__enemies: list[Enemy] = []

        self.__enemies.append(Enemy(self.__world, self.__world.getPositionAtCoordinate(
            0, 16), 50.0, GRID_SIZE.x / 2 - 4))
        self.__enemies.append(Enemy(self.__world, self.__world.getPositionAtCoordinate(
            3, 5), 100.0, GRID_SIZE.x / 2 - 4))
        
        self.__bombs : list[Bomb] = []
        self.__particle_systems : list[ParticleSystem] = []

    def __calculateDeltaTime(self):
        self.__delta_time = time.time() - self.__previous_frame_time
        self.__previous_frame_time = time.time()

    def __pause(self):
        self.__is_paused = True

    def __resume(self):
        self.__is_paused = False

    def __reset(self):
        pass

    def __startGame(self):
        self.__game_state = self.GameState.GAMEPLAY

    def __gameOver(self):
        pass

    def __handleEvents(self, events):
        # mousePos = Vector2(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])

        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_p:
                if self.__game_state == self.GameState.MENU:
                    self.__startGame()
                elif self.__game_state == self.GameState.GAMEPLAY:
                    if self.__is_paused:
                        self.__resume()
                    else:
                        self.__pause()
                else:
                    self.__reset()
                    self.__startGame()
                    
            if event.type == pg.KEYDOWN and event.key == pg.K_b:
                self.__bombs.append(Bomb(self.__player.position, GRID_SIZE.x / 2.0))

            if event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                self.__desired_move_dir = Character.MoveDirection.LEFT
                self.__last_key_pressed_timer = self.__retain_key_pressed_duration
            if event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                self.__desired_move_dir = Character.MoveDirection.RIGHT
                self.__last_key_pressed_timer = self.__retain_key_pressed_duration
            if event.type == pg.KEYDOWN and event.key == pg.K_UP:
                self.__desired_move_dir = Character.MoveDirection.UP
                self.__last_key_pressed_timer = self.__retain_key_pressed_duration
            if event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                self.__desired_move_dir = Character.MoveDirection.DOWN
                self.__last_key_pressed_timer = self.__retain_key_pressed_duration

    def __drawMenuScreen(self):
        pos = self.__renderer.screenSize()/2.0 + Vector2(0, 40)
        self.__renderer.renderText(
            TITLE, pos, font_size=30, color=YELLOW)
        self.__renderer.renderText(
            "Press key 'p' to play", pos - Vector2(0, 40), font_size=20, color=YELLOW)

        self.__renderer.renderText(
            "Press key 'esc' to quit", pos - Vector2(0, 80), font_size=20, color=YELLOW)

    def __drawGameplayScreen(self):
        if self.__is_paused:
            pos = self.__renderer.screenSize()/2.0 + Vector2(0, 40)
            self.__renderer.renderText("PAUSED", pos, 30, color=YELLOW)
            self.__renderer.renderText(
                "Press key 'p' to resume", pos - Vector2(0, 40), 20, color=YELLOW)
        else:
            for enemy in self.__enemies:
                enemy.targetPlayer(self.__player)
                enemy.update(self.__delta_time)
                enemy.draw(self.__renderer)
            
            for ps in self.__particle_systems:
                ps.update(self.__delta_time)
                ps.draw(self.__renderer)
            
            for b in self.__bombs:
                b.update(self.__delta_time)
                if b.life_timer > b.life_time:
                    self.__particle_systems.append(b.explode())
                b.draw(self.__renderer)
                
            self.__player.update(self.__delta_time)
            self.__player.draw(self.__renderer)

            cnt = len(self.__bombs)
            
            for i in range(cnt):
                if self.__bombs[cnt-i-1].is_exploded:
                    self.__bombs.pop(cnt-i-1)


    def __drawGameoverScreen(self):
        self.__renderer.renderText(
            "GAME OVER", self.__renderer.screenSize()/2.0, font_size=30, color=YELLOW)
    
    def update(self, events):
        self.__calculateDeltaTime()
        self.__handleEvents(events)

        self.__display_surface.fill(MAXIMUM_BLUE)

        self.__world.draw(self.__renderer)

        self.__last_key_pressed_timer -= self.__delta_time

        if self.__last_key_pressed_timer < 0:
            self.__desired_move_dir = Character.MoveDirection.NONE

        self.__player.desired_dir = self.__desired_move_dir

        if self.__game_state == self.GameState.MENU:
            self.__drawMenuScreen()
        elif self.__game_state == self.GameState.GAMEPLAY:
            self.__drawGameplayScreen()
        else:
            self.__drawGameoverScreen()

        pg.display.update()
