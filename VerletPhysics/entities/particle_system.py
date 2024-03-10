from typing import List
from pygame import Vector2
import random
import pymunk
from pymunk.body import Body
from pymunk.space import Space

from entities.entity import Entity
from renderer import Renderer
from utilities.colors import CULTURED, WHITE


class Particle(Entity):
    def __init__(self, pos: Vector2, velocity: Vector2, acceleration: Vector2, size: float, life_time=5, color=WHITE):
        super().__init__(pos, 0, color=color)
        self.velocity = velocity
        self.acceleration = acceleration
        self.size = size
        self.__life_time = life_time
        self.__timer = 0

    @property
    def lifeTime(self):
        return self.__life_time

    @property
    def timer(self):
        return self.__timer

    def update(self, delta_time):
        self.__timer += delta_time

    def draw(self, renderer: Renderer):
        renderer.renderCircle(self.position, self.size, self.color)


class RigidParticle(Particle):
    def __init__(self, pos: Vector2, velocity: Vector2, acceleration: Vector2, size: float, space: Space, life_time=5, color=WHITE):
        super().__init__(pos, velocity, acceleration,
                         size, life_time=life_time, color=color)
        self.body = Body()
        self.body.position = pos.x, pos.y
        self.body.velocity = velocity.x, velocity.y
        self.shape = pymunk.Circle(self.body, size)
        self.shape.filter = pymunk.ShapeFilter(categories=8, mask=5)
        self.shape.mass = 1
        self.shape.elasticity = 0
        space.add(self.body, self.shape)

    def draw(self, renderer: Renderer):
        renderer.renderCircle(self.body.position,
                              self.shape.radius, self.color)


class ParticleSystem:
    def __init__(self, max_count: int = 10, life_time: float = 10.0, color=WHITE):
        self._life_time = life_time
        self.timer = 0
        self.max_count = max_count
        self._particles: list[Particle] = []
        self.color = color

    @property
    def lifeTime(self):
        return self._life_time

    @property
    def particleCount(self) -> int:
        return len(self._particles)

    @property
    def particles(self):
        return self._particles

    def addParticle(self, pos, velocity, acceleration, size, color=None):
        par_color = self.color if color is None else color
        particle = Particle(pos, velocity, acceleration, size, par_color)
        self._particles.append(particle)

    def removeParticle(self, particle):
        if self._particles.__contains__(particle):
            self._particles.remove(particle)

    def destroy(self):
        self._particles = []

    def update(self, delta_time):
        self.timer += delta_time
        removable_particles = []
        for p in self._particles:
            if p.timer > p.lifeTime:
                removable_particles.append(p)
                continue
            p.update(delta_time)

        for p in removable_particles:
            self.removeParticle(p)

    def draw(self, renderer: Renderer):
        for p in self._particles:
            p.draw(renderer)


class BurstParticleSysytem(ParticleSystem):
    def __init__(self, pos, space: Space, min_life_time: float = 5, max_life_time: float = 10, max_count: int = 10, color=WHITE):
        super().__init__(max_count=max_count, life_time=max_life_time, color=color)
        self.__space = space
        self.min_life_time = min_life_time
        self.max_life_time = max_life_time
        for i in range(max_count):
            r1 = random.random()
            r2 = random.random()
            r3 = random.random()
            vel = Vector2((0.5 - r1) * 300, 300 + r2 * 400)
            acc = Vector2(0, -981)
            size = 3 + r3 * 7
            self.addParticle(pos, vel, acc, size, space, color=color)

    def addParticle(self, pos, velocity, acceleration, size, space, color=None):
        life_time = self.min_life_time + random.random() * (self.max_life_time -
                                                            self.min_life_time)
        par_color = self.color if color is None else color
        particle = RigidParticle(
            pos, velocity, acceleration, size, space, life_time=life_time, color=par_color)
        self._particles.append(particle)

    def removeParticle(self, particle):
        if self.__space.bodies.__contains__(particle.body):
            self.__space.remove(particle.body, particle.shape)
        super().removeParticle(particle)

    def destroy(self):
        for p in self._particles:
            if self.__space.bodies.__contains__(p.body):
                self.__space.remove(p.body)
        super().destroy()

    def update(self, delta_time):
        super().update(delta_time)
        for p in self._particles:
            def update_velocity(body, gravity, damping, dt):
                pymunk.Body.update_velocity(
                    body, (p.acceleration.x, p.acceleration.y), damping, dt)

            p.body.velocity_func = update_velocity


class IntervalParticleSystem(ParticleSystem):
    def __init__(self, pos, space: Space, count=10, max_count: int = 10, interval_time: float = 1, color=WHITE):
        super().__init__(max_count=max_count, life_time=0, color=color)
        self.__space = space
        self.count = count
        self.interval_time = interval_time

    def addParticle(self, pos, velocity, acceleration, size, life_time=5, color=WHITE):
        par_color = self.color if color is None else color
        particle = RigidParticle(
            pos, velocity, acceleration, size, self.__space, life_time, par_color)
        self._particles.append(particle)

    def removeParticle(self, particle):
        if self.__space.bodies.__contains__(particle.body):
            self.__space.remove(particle.body, particle.shape)
        super().removeParticle(particle)

    def destroy(self):
        for p in self._particles:
            if self.__space.bodies.__contains__(p.body):
                self.__space.remove(p.body)
        super().destroy()

    def update(self, delta_time):
        super().update(delta_time)
        for p in self._particles:
            def update_velocity(body, gravity, damping, dt):
                pymunk.Body.update_velocity(
                    body, (p.acceleration.x, p.acceleration.y), damping, dt)

            p.body.velocity_func = update_velocity
