from enum import Enum
import time
import pygame as pg
from pygame import Vector2, mixer

from entities.body import BodyType
from entities.dot import Dot
from entities.entity import Entity, SpecialEntity
from entities.spring import Spring

from settings import TITLE
from renderer import Renderer
from utilities.colors import *
from utilities.physics import Physics


class Game:
    class GameState(Enum):
        MENU = 0
        GAMEPLAY = 1
        GAMEOVER = 2

    def __init__(self):
        self.__display_surface = Renderer.getInstance().surface
        self.__is_paused = False
        self.__game_state = self.GameState.MENU

        self.__space = Physics(gravity=Vector2(0, -50))
        self.__entities: list[Entity] = []

        self.__previous_frame_time = time.time()

        self.__createScene()

        for ent in self.__entities:
            self.__space.addEntity(ent)

        # mixer.music.load("assets/background_music.wav")
        # self.__collect_sound = mixer.Sound("assets/collect.wav")
        # self.__health_loss_sound = mixer.Sound("assets/health_loss.wav")
        # self.__gameover_sound = mixer.Sound("assets/gameover.wav")
        # mixer.music.play(-1)
        # mixer.music.set_volume(0)

    def __createScene(self):
        self.__entities.append(self.__createRectangularShape(
            Renderer.getInstance().screenSize / 2, Vector2(100, 60)))
        self.__entities.append(self.__createPlatform(
            Vector2(Vector2(Renderer.getInstance().screenSize.x / 2, 40), 150), Vector2(Renderer.getInstance().screenSize.x - 10, 40)))
        self.__entities.append(self.__createStick())
        pass
        # dots: list[Dot] = []
        # dots.append(Dot(Vector2(400, 400), 5, color=BLACK,
        #                 body_type=BodyType.STATIC))
        # dots.append(Dot(Vector2(400, 300), 10, color=BLUE_RYB))
        # self.__spring = Entity(dots)
        # self.__spring.addSpring(Spring(dots[0], dots[1]))

        # self.__entities.append(self.__spring)
        # self.__entities.append(self.__createPlatform(Vector2(400, 40),Vector2(780, 30)))
        # self.__entities.append(
        #     self.__createStarShape(Vector2(250, 300), 60, 30))
        # self.__entities.append(self.__createStarShape(
        #     Vector2(400, 300), 60, 30, 4))
        # self.__entities.append(self.__createRoundedRectangularShape())
        # self.__entities.append(self.__createStick())
        # self.__entities.append(self.__createRectangularShape())
        # self.__entities.append(self.__createPlatform(
        #     Vector2(130, 150), Vector2(240, 40)))
        # self.__entities.append(self.__createPlatform(
        #     Vector2(800-130, 80), Vector2(240, 40)))

        # self.__entities.append(self.__createRectangularShape(Vector2(400, 400), Vector2(
        #     450, 60), row_divide=1, column_divide=20))

    def __createPlatform(self, pos: Vector2, size: Vector2):
        dots: list[Dot] = []

        half_size = size / 2

        lf_bt_pos = pos - half_size
        rt_bt_pos = pos + Vector2(half_size.x, -half_size.y)
        lf_tp_pos = pos + Vector2(-half_size.x, half_size.y)
        rt_tp_pos = pos + half_size

        dot = Dot(lf_bt_pos, body_type=BodyType.STATIC)
        dots.append(dot)

        dot = Dot(rt_bt_pos, body_type=BodyType.STATIC)
        dots.append(dot)

        dot = Dot(rt_tp_pos, body_type=BodyType.STATIC)
        dots.append(dot)

        dot = Dot(lf_tp_pos, body_type=BodyType.STATIC)
        dots.append(dot)

        return Entity(dots, body_type=BodyType.STATIC)

    def __createRectangularShape(self, pos: Vector2, size: Vector2, row_divide: int = 1, column_divide: int = 1):
        dots: list[Dot] = []

        lt_bt_pos = pos - size / 2
        cell_size = Vector2(size.x / column_divide, size.y / row_divide)

        for i in range(0, row_divide+1):
            for j in range(0, column_divide+1):
                pt = Vector2(lt_bt_pos.x + j * cell_size.x,
                             lt_bt_pos.y + i * cell_size.y)
                dot = Dot(pt, body_type=BodyType.DYNAMIC)
                dots.append(dot)

        ent = SpecialEntity(dots, row_divide, column_divide, fill_color=YELLOW)

        for i in range(0, row_divide+1):
            for j in range(0, column_divide+1):
                if j > 0:
                    ent.addSpring(
                        Spring(dots[i * (column_divide + 1) + j-1], dots[i * (column_divide + 1) + j]))

                if i > 0:
                    ent.addSpring(
                        Spring(dots[(i-1) * (column_divide+1)+j], dots[i * (column_divide+1)+j]))

                if j < column_divide:
                    if i < row_divide:
                        ent.addSpring(
                            Spring(dots[i * (column_divide+1)+j], dots[(i + 1) * (column_divide+1)+j + 1]))

                    if i > 0:
                        ent.addSpring(
                            Spring(dots[i * (column_divide+1)+j], dots[(i - 1) * (column_divide+1)+j + 1]))

        return ent

    def __createStick(self):
        points = [Vector2(100, 300), Vector2(100, 400)]

        dots: list[Dot] = []

        for pt in points:
            dot = Dot(pt, body_type=BodyType.DYNAMIC)
            dots.append(dot)

        ent = Entity(dots)

        ent.addSpring(Spring(dots[0], dots[1]))

        return ent

    def __createRoundedRectangularShape(self):
        pass
        # points = [Vector2(100, 100), Vector2(150, 100), Vector2(170, 120), Vector2(
        #     170, 180), Vector2(150, 200), Vector2(100, 200), Vector2(80, 180), Vector2(80, 120)]

        # dots: list[Dot] = []

        # for pt in points:
        #     dot = Dot(pt, body_type=BodyType.DYNAMIC)
        #     dots.append(dot)

        # ent = Entity(dots)

        # for i in range(0, len(dots)):
        #     for j in range(i+1, len(dots)):
        #         ent.addSpring(Spring(dots[i], dots[j]))

        # return ent

    def __createStarShape(self, center: Vector2, mx_dst: float, mi_dst: float, number_of_petals: int = 6):
        pass
        # angle_per_half_petal = 360 / (2 * number_of_petals)
        # angle = 0
        # isMax = True

        # dots: list[Dot] = []

        # while angle < 360:
        #     a = angle * math.pi / 180
        #     pt = center + Vector2(mx_dst * math.cos(a), mx_dst * math.sin(a))

        #     if not isMax:
        #         pt = center + Vector2(mi_dst * math.cos(a),
        #                               mi_dst * math.sin(a))

        #     dot = Dot(pt, body_type=BodyType.DYNAMIC)
        #     dots.append(dot)

        #     isMax = not isMax
        #     angle += angle_per_half_petal

        # ent = Entity(dots)

        # for i in range(0, len(dots)):
        #     for j in range(i+1, len(dots)):
        #         ent.addSpring(Spring(dots[i], dots[j]))

        # return ent

    def __calculateDeltaTime(self):
        self.__delta_time = time.time() - self.__previous_frame_time
        # self.__delta_time *= 60
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
        self.__game_state = self.GameState.GAMEOVER

    def __handleEvents(self, events):
        self.__mousePos = Vector2(
            pg.mouse.get_pos()[0], Renderer.getInstance().screenSize.y - pg.mouse.get_pos()[1])

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

    def __drawMenuScreen(self):
        pos = Renderer.getInstance().screenSize/2.0 + Vector2(0, 40)
        Renderer.getInstance().renderText(
            TITLE, pos, font_size=30, color=YELLOW)
        Renderer.getInstance().renderText(
            "Press key 'p' to play", pos - Vector2(0, 40), font_size=20, color=YELLOW)

        Renderer.getInstance().renderText(
            "Press key 'esc' to quit", pos - Vector2(0, 80), font_size=20, color=YELLOW)

    def __drawGameplayScreen(self, delta_time):
        pass

    def __drawGameoverScreen(self):
        Renderer.getInstance().renderText(
            "GAME OVER", Renderer.getInstance().screenSize/2.0, font_size=30, color=YELLOW)

    def update(self, events, delta_time):
        self.__calculateDeltaTime()
        self.__handleEvents(events)

        self.__display_surface.fill(RED_ORANGE_COLOR)

        if self.__game_state == self.GameState.MENU:
            self.__drawMenuScreen()
        elif self.__game_state == self.GameState.GAMEPLAY:
            self.__drawGameplayScreen(delta_time)

            if not self.__is_paused:
                self.__space.step(self.__delta_time)

            for ent in self.__entities:
                ent.draw(Renderer.getInstance(), True)

            Renderer.getInstance().renderGizmos(delta_time)
        else:
            self.__drawGameoverScreen()

        pg.display.update()
