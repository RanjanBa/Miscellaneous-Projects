from enum import Enum
import time
import math
from random import randint, random
import pygame as pg
from pygame import Rect, Vector2, mixer
from pygame.draw import circle
import pymunk
from pymunk.body import Body
import pymunk.pygame_util
from effect import CircleEffect
from entities.entity import RigidBody
from entities.particle_system import BurstParticleSysytem, IntervalParticleSystem, ParticleSystem, Particle, RigidParticle
from entities.triangle import Trianlge

from entities.player import Player
from renderer import Renderer
from utilities.colors import *
from entities.rectangle import Rectangle
from entities.circle import Circle
from settings import TITLE


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
        self.__spawn_duration = 1
        self.__spawn_timer = 0
        self.__delta_time = 0
        self.__wall_width = 20
        self.__ground_width = 20
        self.__score = 0
        self.__max_life = 5
        self.__life_left_over = self.__max_life
        self.__player_size = Vector2(40, 60)
        self.__player_spawn_pos = Vector2(self.__renderer.screenSize().x / 2, 60 + 20)

        self.__colors = [CELADON, POWDER_BLUE,
                         CULTURED, HOT_PINK, MAXIMUM_BLUE_PURPLE, LIGHT_GREEN, PASTEL_PINK]  # BLUE_RYB

        self.__previous_frame_time = time.time()
        self.__wall_or_grounds = {}
        self.__dynamic_entities = {}

        self.__space = pymunk.Space()
        self.__space.gravity = 0, -100

        self.__setUpWorld()

        # self.__draw_options = pymunk.pygame_util.DrawOptions(
        #     self.__renderer.surface)

        self.__effects: list[CircleEffect] = []
        self.__particle_systems: list[BurstParticleSysytem] = []
        self.__snow_particle_system = IntervalParticleSystem(Vector2(
            0, 0), self.__space, 1, 500, 0.2, color=CULTURED)
        self.show_instructions = True
        self.__flashTimer = 0
        self.__visible_instruction = True
        mixer.music.load("assets/background_music.wav")
        self.__collect_sound = mixer.Sound("assets/collect.wav")
        self.__health_loss_sound = mixer.Sound("assets/health_loss.wav")
        self.__gameover_sound = mixer.Sound("assets/gameover.wav")
        mixer.music.play(-1)
        mixer.music.set_volume(0.5)

    def __createCircle(self, pos : Vector2, radius: float, color=YELLOW, body_type=pymunk.Body.DYNAMIC):
        circle = Circle(pos, radius, color=color, body_type=body_type)
        circle.shape.density = 1
        circle.shape.friction = 1
        circle.shape.filter = pymunk.ShapeFilter(1)

        self.__space.add(circle.body, circle.shape)

        return circle

    def __createRectangle(self, pos : Vector2, size, angle=0, color=BLUE, body_type=pymunk.Body.DYNAMIC):
        pos = pos - size / 2
        rectangle = Rectangle(Rect(pos, size), angle,
                              color=color, body_type=body_type)
        rectangle.shape.density = 1
        rectangle.shape.friction = 1
        rectangle.shape.filter = pymunk.ShapeFilter(1)

        self.__space.add(rectangle.body, rectangle.shape)

        return rectangle

    def __createTriangle(self, pos : Vector2, length: float, angle=0, color=GREEN, body_type=pymunk.Body.DYNAMIC):
        triangle = Trianlge(pos, length, angle, color, body_type)
        triangle.shape.density = 1
        triangle.shape.friction = 1
        triangle.shape.filter = pymunk.ShapeFilter(1)

        self.__space.add(triangle.body, triangle.shape)
        return triangle

    def __setUpPlayer(self):
        self.__player = Player(self, self.__space, self.__player_spawn_pos, self.__player_size,
                               BLUE_RYB)

    def __setUpWorld(self):
        self.__setUpPlayer()

        # Ground
        rectangle = self.__createRectangle(
            Vector2(self.__renderer.screenSize().x/2, self.__ground_width / 2.0), Vector2(self.__renderer.screenSize().x, self.__ground_width), color=YALE_BLUE, body_type=pymunk.Body.STATIC)
        rectangle.shape.filter = pymunk.ShapeFilter(categories=4, mask=9)
        self.__wall_or_grounds[rectangle.body] = rectangle

        # Left Wall
        rectangle = self.__createRectangle(
            Vector2(self.__wall_width / 2.0, self.__renderer.screenSize().y / 2), Vector2(self.__wall_width, self.__renderer.screenSize().y), color=YALE_BLUE, body_type=pymunk.Body.STATIC)
        rectangle.shape.filter = pymunk.ShapeFilter(categories=4, mask=9)
        self.__wall_or_grounds[rectangle.body] = rectangle

        # Right Wall
        rectangle = self.__createRectangle(
            Vector2(self.__renderer.screenSize().x - self.__wall_width / 2.0, self.__renderer.screenSize().y / 2), Vector2(self.__wall_width, self.__renderer.screenSize().y), color=YALE_BLUE, body_type=pymunk.Body.STATIC)
        rectangle.shape.filter = pymunk.ShapeFilter(categories=4, mask=9)
        self.__wall_or_grounds[rectangle.body] = rectangle

    def __calculateDeltaTime(self):
        self.__delta_time = time.time() - self.__previous_frame_time
        # self.__delta_time *= 60
        self.__previous_frame_time = time.time()

    def __pause(self):
        self.__is_paused = True

    def __resume(self):
        self.__is_paused = False

    def __reset(self):
        self.__score = 0
        self.__flashTimer = 0
        self.__life_left_over = self.__max_life
        self.__particle_systems = []

    def __startGame(self):
        self.__game_state = self.GameState.GAMEPLAY
        self.__dynamic_entities[self.__player.body] = self.__player
        self.__space.add(self.__player.body, self.__player.shape)
        self.__player.body.velocity = (0, 0)
        self.show_instructions = True
        self.__flashTimer = 0
        self.__visible_instruction = True
        self.__player.reset()

    def __gameOver(self):
        if self.__space.bodies.__contains__(self.__player.body):
            self.__space.remove(self.__player.body, self.__player.shape)
        self.__dynamic_entities.pop(self.__player.body)
        for body in self.__dynamic_entities:
            if self.__space.bodies.__contains__(body):
                self.__space.remove(body)

        self.__dynamic_entities = {}
        self.__game_state = self.GameState.GAMEOVER
        self.__player.reset()

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

    def __drawMenuScreen(self):
        pos = self.__renderer.screenSize()/2.0 + Vector2(0, 40)
        self.__renderer.renderText(
            TITLE, pos, font_size=30, color=YELLOW)
        self.__renderer.renderText(
            "Press key 'p' to play", pos - Vector2(0, 40), font_size=20, color=YELLOW)

        self.__renderer.renderText(
            "Press key 'esc' to quit", pos - Vector2(0, 80), font_size=20, color=YELLOW)

    def __drawGameplayScreen(self, delta_time):
        self.__renderer.renderText("Spawn Timer : {0:0.2f}".format(
            self.__spawn_timer), Vector2(100, self.__renderer.screenSize().y - 20), font_size=18, color=TEAL)
        self.__renderer.renderText("Score : {0}".format(self.__score), Vector2(
            self.__renderer.screenSize().x/2, self.__renderer.screenSize().y - 20), 20, color=TEAL)
        self.__renderer.renderText("Lifes : {0}".format(self.__life_left_over), Vector2(
            self.__renderer.screenSize().x - 100, self.__renderer.screenSize().y - 20), 20, color=TEAL)
        if self.__is_paused:
            pos = self.__renderer.screenSize()/2.0 + Vector2(0, 40)
            self.__renderer.renderText("PAUSED", pos, 30, color=YELLOW)
            self.__renderer.renderText(
                "Press key 'p' to resume", pos - Vector2(0, 40), 20, color=YELLOW)
        else:
            self.__flashTimer += delta_time
            if self.__flashTimer >= 0.3:
                self.__visible_instruction = not self.__visible_instruction
                self.__flashTimer -= 0.3

        if self.__visible_instruction and not self.__is_paused and self.show_instructions:
            pos = self.__renderer.screenSize()/2.0 + Vector2(0, 40)
            self.__renderer.renderText(
                TITLE, Vector2(pos.x, self.__renderer.screenSize().y - 60), font_size=30, color=BLUE)
            
            pos = self.__renderer.screenSize()/2.0 + Vector2(0, 40)
            self.__renderer.renderText(
                "Press Left Arrow Key to move left.", pos, 18, color=RED)
            pos.y -= 30
            self.__renderer.renderText(
                "Press Right Arrow Key to move right.", pos, 18, color=RED)

    def __drawGameoverScreen(self):
        self.__renderer.renderText(
            "GAME OVER", self.__renderer.screenSize()/2.0, font_size=30, color=YELLOW)

    def __spawnFalling(self):
        while self.__spawn_timer >= self.__spawn_duration:
            self.__spawn_timer -= self.__spawn_duration
            r = randint(0, 2)
            r_c = randint(0, len(self.__colors) - 1)
            pos = Vector2(self.__wall_width + random() * (self.__renderer.screenSize().x - 2 * self.__wall_width),
                          self.__renderer.screenSize().y)
            rg_body: RigidBody = None
            if r == 0:
                radius = 30 + random() * 20
                pos.x = max(radius + self.__wall_width, min(pos.x,
                                                            self.__renderer.screenSize().x - radius - self.__wall_width))
                rg_body = self.__createCircle(
                    pos, radius, color=self.__colors[r_c])
            elif r == 1:
                length = 30 + random() * 20
                pos.x = max(length + self.__wall_width, min(pos.x,
                                                            self.__renderer.screenSize().x - length - self.__wall_width))
                rg_body = self.__createTriangle(
                    pos, length, random() * math.radians(360), color=self.__colors[r_c])
            else:
                size = Vector2(30 + random() * 20, 30 + random() * 20)
                pos.x = max(size.x + self.__wall_width, min(pos.x,
                                                            self.__renderer.screenSize().x - size.x - self.__wall_width))
                rg_body = self.__createRectangle(
                    pos, size, angle=random() * math.radians(360), color=self.__colors[r_c])

            rg_body.shape.filter = pymunk.ShapeFilter(categories=2, mask=1)
            self.__dynamic_entities[rg_body.body] = rg_body

    def __spawnSnowParticleSystem(self):
        if self.__snow_particle_system.timer < self.__snow_particle_system.interval_time:
            return
        self.__snow_particle_system.timer = 0.0
        for i in range(self.__snow_particle_system.count):
            if self.__snow_particle_system.particleCount >= self.__snow_particle_system.max_count:
                break
            pos = Vector2(random() * self.__renderer.screenSize().x,
                          self.__renderer.screenSize().y + random() * 50)
            vel = Vector2((0.5 - random()) * 20, - 30 - random() * 30)
            acc = Vector2((0.5 - random()) * 20, -10 - random() * 30)
            # acc = Vector2(0, -100)
            size = 1 + random() * 5
            self.__snow_particle_system.addParticle(
                pos, vel, acc, size, life_time=8.0, color=CULTURED)

    def __spawnBurstParticleSystem(self, body, contact_point):
        color = self.__dynamic_entities[body].color
        self.__effects.append(CircleEffect(
            contact_point + Vector2(0, 20), 20, 15, 10, color=color))
        self.__particle_systems.append(BurstParticleSysytem(
            contact_point, self.__space, 4, 8, 20, color=color))

    def update(self, events, delta_time):
        self.__calculateDeltaTime()
        self.__handleEvents(events)
        # if self.__snow_particle_system.timer >= self.__snow_particle_system.interval_time:
        self.__spawnSnowParticleSystem()

        self.__display_surface.fill(MAXIMUM_BLUE)

        if not self.__is_paused:
            self.__snow_particle_system.update(self.__delta_time)

        removable_particle_systems: list[BurstParticleSysytem] = []
        for ps in self.__particle_systems:
            if ps.timer >= ps.lifeTime:
                removable_particle_systems.append(ps)
                continue
            ps.update(self.__delta_time)

        for ps in removable_particle_systems:
            ps.destroy()
            self.__particle_systems.remove(ps)

        if not self.__is_paused:
            self.__space.step(self.__delta_time)

        for key, value in self.__dynamic_entities.items():
            value.draw(self.__renderer)
        for key, value in self.__wall_or_grounds.items():
            value.draw(self.__renderer)

        for ps in self.__particle_systems:
            ps.draw(self.__renderer)

        if self.__game_state == self.GameState.MENU:
            self.__drawMenuScreen()
        elif self.__game_state == self.GameState.GAMEPLAY:
            if not self.__is_paused:
                self.__spawn_timer += self.__delta_time
                if self.__spawn_timer >= self.__spawn_duration:
                    self.__spawnFalling()

                def f(arbiter):
                    n = -arbiter.contact_point_set.normal
                    # print(arbiter.shapes[1].body._id)
                    if arbiter.shapes[1].body.body_type == 0 and self.__space.bodies.__contains__(arbiter.shapes[1].body):
                        if self.__dynamic_entities.__contains__(arbiter.shapes[1].body):
                            self.__score += 1
                            self.__collect_sound.play()
                            self.__spawnBurstParticleSystem(arbiter.shapes[1].body, Vector2(
                                arbiter.contact_point_set.points[0].point_b))
                            self.__space.remove(
                                arbiter.shapes[1], arbiter.shapes[1].body)
                            self.__dynamic_entities.pop(
                                arbiter.shapes[1].body)

                self.__player.body.each_arbiter(f)
                self.__player.update(events, delta_time, self.__renderer)

                removable_bodies: list[Body] = []
                for body in self.__space.bodies:
                    if body.position.y < -10.0:
                        removable_bodies.append(body)

                for body in removable_bodies:
                    for s in body.shapes:
                        self.__space.remove(s)
                    self.__space.remove(body)
                    if self.__dynamic_entities.__contains__(body):
                        self.__life_left_over -= 1
                        self.__health_loss_sound.play()
                        self.__dynamic_entities.pop(body)
                        if self.__life_left_over < 0:
                            self.__gameOver()
                            self.__gameover_sound.play()
            self.__drawGameplayScreen(delta_time)
        else:
            self.__drawGameoverScreen()

        # self.__space.debug_draw(self.__draw_options)
        # print(len(self.__space.bodies), len(self.__space.shapes))
        self.__snow_particle_system.draw(self.__renderer)
        removable_effects = []
        for effect in self.__effects:
            effect.draw(self.__delta_time, self.__renderer)
            if effect.timer > effect.life_time:
                removable_effects.append(effect)

        for effect in removable_effects:
            self.__effects.remove(effect)
        pg.display.update()
