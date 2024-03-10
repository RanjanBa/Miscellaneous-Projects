from typing import List
from pygame.constants import K_LEFT, K_RIGHT, K_SPACE
# from pygame.draw import line, lines
import pymunk
import pygame as pg
from pygame import Rect, Vector2, mixer
from effects.particle_system import JumpEffect

from entities.entity import RigidBody
from entities.rectangle import Rectangle
from renderer import Renderer
from utilities.colors import BLUE, WHITE

import settings

class Player(RigidBody):
    def __init__(self, game, space: pymunk.Space, pos: Vector2, size=Vector2(40, 60), color=WHITE):
        self.__game = game
        self.__space = space
        self.__size = size
        self.__initial_position = pos
        shape = pymunk.Poly.create_box(None, self.__size)
        super().__init__(pos, 0, shape, color=color, body_type=pymunk.Body.KINEMATIC)
        shape.mass = 1
        shape.filter = pymunk.ShapeFilter(categories=1, mask=15)
        self.__is_left_key_pressed = False
        self.__is_right_key_pressed = False
        self.__directional_input = Vector2(0, 0)
        self.__max_speed = 0
        self.__jump_force = 600
        self.__jump_cutoff_percent = 0.5
        self.__gravity = -981
        self.__velocity = Vector2(0, 0)
        self.__air_jump_max_count = 3
        self.__air_jump_left = 0
        self.__jump_buffer_time = 0.2
        self.__cyote_time = 0.2
        self.__on_air_timer = 2 * self.__cyote_time
        self.__jump_key_pressed_passed_time = 2 * self.__jump_buffer_time
        self.__skin_width = 2.0
        self.__grounded_platform = None
        self.render_lines = []
        self.__is_grounded = False
        self.__jump_sound = mixer.Sound("assets/player_jump.wav")
        self.__land_sound = mixer.Sound("assets/player_land.wav")
        self.__jump_particle_systems: List[JumpEffect] = []

    def __handleEvents(self, events):
        self.__directional_input = Vector2(0, 0)
        for event in events:
            if event.type == pg.KEYDOWN and event.key == K_LEFT:
                self.__is_left_key_pressed = True

            if event.type == pg.KEYDOWN and event.key == K_RIGHT:
                if not self.__is_left_key_pressed:
                    self.__is_right_key_pressed = True

            if event.type == pg.KEYUP and event.key == K_LEFT:
                self.__is_left_key_pressed = False
            if event.type == pg.KEYUP and event.key == K_RIGHT:
                self.__is_right_key_pressed = False

            if event.type == pg.KEYDOWN and event.key == K_SPACE:
                self.__jump_key_pressed_passed_time = 0.0
            if event.type == pg.KEYUP and event.key == K_SPACE:
                if self.__velocity.y > 0:
                    self.__velocity.y *= (1 - self.__jump_cutoff_percent)

        if self.__is_left_key_pressed:
            self.__game.show_instructions = False
            self.__directional_input.x = -1.0
        if self.__is_right_key_pressed:
            self.__directional_input.x = 1.0
            self.__game.show_instructions = False

    def __raycast(self, start_pos, dir, distance, platforms, renderer):
        end_pos = start_pos + dir * distance
        # renderer.renderLine(start_pos, end_pos, YELLOW, 3)
        qs = self.__space.segment_query(
            (start_pos.x, start_pos.y), (end_pos.x, end_pos.y), 1, pymunk.ShapeFilter())

        if qs != None:
            for q in qs:
                if q.shape is not self.shape:
                    for plat in platforms:
                        if q.shape.body == plat.body:
                            if Rect(plat.position - plat.size / 2, plat.size).colliderect(Rect(self.position - self.__size / 2, self.__size)):
                                return None
                    return q
        return None

    def __jump(self):
        self.__velocity = Vector2(self.__velocity.x, self.__jump_force)
        self.__jump_key_pressed_passed_time = 2 * self.__jump_buffer_time
        self.__on_air_timer = 2 * self.__cyote_time
        self.__jump_sound.set_volume(settings.VOLUME)
        self.__jump_sound.play()
        self.__jump_particle_systems.append(JumpEffect(self.position - Vector2(0, 0.5) * self.__size.y,
                                                       Vector2(-100, 0), Vector2(-100, -200), 10, velocity_range=Vector2(200, 100), count=100))

    @property
    def isGrounded(self):
        return self.__is_grounded

    @property
    def groundedPlatform(self) -> Rectangle:
        return self.__grounded_platform

    def reset(self):
        self.__directional_input = Vector2(0, 0)
        self.__velocity = Vector2(0, 0)
        self.__is_left_key_pressed = False
        self.__is_right_key_pressed = False
        self.body.position = (self.__initial_position.x,
                              self.__initial_position.y)
        self.__jump_particle_systems = []

    def update(self, platforms, events, delta_time, renderer: Renderer):
        self.__handleEvents(events)

        if self.__jump_key_pressed_passed_time < self.__jump_buffer_time:
            if self.__is_grounded:
                self.__jump()
            else:
                if self.__on_air_timer < self.__cyote_time:
                    self.__jump()
                elif self.__air_jump_left > 0:
                    self.__jump()
                    self.__air_jump_left -= 1

        self.__velocity.y += self.__gravity * delta_time
        self.__velocity.x = self.__max_speed * self.__directional_input.x

        # horizontal raycast
        max_horizontal_dist = 0
        if abs(self.__velocity.x) > 0.01:
            distance = abs(self.__velocity.x) * delta_time + self.__skin_width
            if self.__velocity.x > 0.01:
                br = self.position + \
                    Vector2(self.__size.x / 2, -self.__size.y / 2)
                ray_origin = Vector2(br)
                q = self.__raycast(ray_origin, Vector2(
                    1, 0), distance, platforms, renderer)
                max_horizontal_dist = abs(self.__velocity.x * delta_time)
                if q is not None:
                    max_horizontal_dist = abs(
                        q.point.x - ray_origin.x) - self.__skin_width
            else:
                bl = self.position - self.__size / 2
                ray_origin = Vector2(bl)
                q = self.__raycast(
                    ray_origin, Vector2(-1, 0), distance, platforms, renderer)
                max_horizontal_dist = abs(self.__velocity.x * delta_time)
                if q is not None:
                    max_horizontal_dist = abs(
                        q.point.x - ray_origin.x) - self.__skin_width
        # vertical raycast
        distance = abs(self.__velocity.y) * delta_time + self.__skin_width
        max_vertical_dist = abs(self.__velocity.y * delta_time)
        previously_grounded = self.__is_grounded
        self.__is_grounded = False
        self.__grounded_platform = None
        if self.__velocity.y <= 0.0:
            bl = self.position - self.__size / 2
            ray_origin = Vector2(bl)
            ray_direction = Vector2(0, -1)
            q = self.__raycast(ray_origin, ray_direction,
                               distance, platforms, renderer)
            if q is not None:
                max_vertical_dist = abs(
                    q.point.y - ray_origin.y) - self.__skin_width
                self.__is_grounded = True
                for plat in platforms:
                    if q.shape.body == plat.body:
                        self.__grounded_platform = plat
            else:
                br = self.position + \
                    Vector2(self.__size.x / 2, -self.__size.y / 2)
                ray_origin = Vector2(br)
                q = self.__raycast(
                    ray_origin, ray_direction, distance, platforms, renderer)
                if q is not None:
                    max_vertical_dist = abs(
                        q.point.y - ray_origin.y) - self.__skin_width
                    self.__is_grounded = True
                    for plat in platforms:
                        if q.shape.body == plat.body:
                            self.__grounded_platform = plat
        else:
            pass
            # tl = self.position + Vector2(-self.__size.x / 2, self.__size.y / 2)
            # ray_origin = Vector2(tl)
            # ray_direction = Vector2(0, 1)
            # q = self.__raycast(ray_origin, ray_direction,
            #                    distance, platforms, renderer)
            # if q is not None:
            #     max_vertical_dist = abs(
            #         q.point.y - ray_origin.y) - self.__skin_width
            # else:
            #     tr = self.position + self.__size / 2
            #     ray_origin = Vector2(tr)
            #     q = self.__raycast(
            #         ray_origin, ray_direction, distance, platforms, renderer)

            #     if q is not None:
            #         max_vertical_dist = abs(
            #             q.point.y - ray_origin.y) - self.__skin_width

        for l in self.render_lines:
            renderer.renderLine(l[0], l[1], BLUE, 3)

        self.body.position = self.body.position + \
            Vector2(0, 1) * max_vertical_dist * (1.0 if self.__velocity.y > 0 else -1.0) + \
            Vector2(1, 0) * max_horizontal_dist * \
            (1.0 if self.__velocity.x >= 0 else -1.0)

        if not previously_grounded and self.__is_grounded:
            self.__land_sound.set_volume(settings.VOLUME)
            self.__land_sound.play()

        if self.__is_grounded:
            self.__velocity.y = 0.0
            self.__on_air_timer = 0.0
            self.__air_jump_left = self.__air_jump_max_count
        else:
            self.__on_air_timer += delta_time

        self.__jump_key_pressed_passed_time += delta_time

        for particle_system in self.__jump_particle_systems:
            particle_system.update(delta_time)

        removable_particle_sys = []
        for particle_system in self.__jump_particle_systems:
            if particle_system.timePassed > particle_system.life_time:
                removable_particle_sys.append(particle_system)

        for particle_system in removable_particle_sys:
            self.__jump_particle_systems.remove(particle_system)

    def draw(self, renderer: Renderer):
        pos = self.position

        right = Vector2(1, 0) * self.__size[0] / 2.0
        up = Vector2(0, 1) * self.__size[1] / 2.0

        right.rotate_ip_rad(self.angle)
        up.rotate_ip_rad(self.angle)

        bl = pos - right - up
        tl = pos - right + up
        br = pos + right - up
        tr = pos + right + up
        renderer.renderPolygon([bl, br, tr, tl], self.color)

        for particle_system in self.__jump_particle_systems:
            particle_system.draw(renderer)
