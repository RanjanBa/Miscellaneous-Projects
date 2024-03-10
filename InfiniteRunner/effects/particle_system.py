from random import random

from abc import ABC, abstractmethod
from typing import List
from pygame import Rect, Vector2

from renderer import Renderer
from settings import SCREEN_SIZE
from utilities.colors import YELLOW


class Particle:
    def __init__(self, pos, velocity, acceleration, color):
        self.position = pos
        self.velocity = velocity
        self.acceleration = acceleration
        self.color = color

    @abstractmethod
    def draw(self, renderer: Renderer):
        pass

    def update(self, delta_time):
        self.velocity += self.acceleration * delta_time
        self.position += self.velocity * delta_time


class CircularParticle(Particle):
    def __init__(self, pos, velocity, acceleration, color, size: float, delta_size: float):
        super().__init__(pos, velocity, acceleration, color)
        self.size = size
        self.delta_size = delta_size

    def draw(self, renderer: Renderer):
        renderer.renderCircle(self.position, self.size / 2, self.color)

    def update(self, delta_time):
        super().update(delta_time)
        self.size -= self.delta_size
        self.size = max(0, self.size)


class RectangularParticle(Particle):
    def __init__(self, pos, velocity, acceleration, color, size: Vector2, delta_size: Vector2):
        super().__init__(pos, velocity, acceleration, color)
        self.size = size
        self.delta_size = delta_size

    def draw(self, renderer: Renderer):
        s = Vector2(self.size, self.size)
        rect = Rect(self.position - s / 2, s)
        renderer.renderRect(rect, self.color)

    def update(self, delta_time):
        super().update(delta_time)
        self.size -= self.delta_size
        self.size = Vector2(max(0, self.size.x), max(0, self.size.y))


class ParticleSystem(ABC):
    def __init__(self, life_time):
        self._particles: List[Particle] = []
        self._time_passed = 0.0
        self.life_time = life_time

    @abstractmethod
    def addParticle(self, pos, vel, acc, color, size, delta_size):
        pass

    @property
    def timePassed(self):
        return self._time_passed

    @abstractmethod
    def draw(self, renderer: Renderer):
        pass

    @abstractmethod
    def update(self):
        pass


class JumpEffect(ParticleSystem):
    def __init__(self, pos, start_velocity, start_acceleration, size, size_range=10, velocity_range=Vector2(20, 20), acceleration_range=Vector2(20, 20), count=10, life_time=5.0):
        super().__init__(life_time)
        for _ in range(count):
            vel = start_velocity + \
                Vector2(random() * velocity_range.x,
                        random() * velocity_range.y)
            acc = start_acceleration + \
                Vector2(random() * acceleration_range.x,
                        random() * acceleration_range.y)

            s = size + random() * size_range

            self.addParticle(pos, vel, acc,
                             (random() * 255, 100, 150), s, delta_size=0.1)

    def addParticle(self, pos, vel, acc, color, size, delta_size):
        self._particles.append(
            CircularParticle(pos, vel, acc, color, size, delta_size))

    def draw(self, renderer: Renderer):
        for particle in self._particles:
            particle.draw(renderer)

    def update(self, delta_time):
        self._time_passed += delta_time
        for particle in self._particles:
            particle.update(delta_time)


class SnowFallEffect(ParticleSystem):
    def __init__(self):
        super().__init__(1000)
        self.start_velocity = Vector2(0, -100)
        self.start_acceleration = Vector2(0, -5)
        self.size = Vector2(3, 10)
        self.size_range = Vector2(2, 5)
        self.delay_time = 0.05
        self._delay_timer = 0

    def addParticle(self, pos, vel, acc, color, size, delta_size):
        vel = vel + Vector2(-20 + random() * 40, -3 * random() + random() * 3)
        self._particles.append(
            RectangularParticle(pos, vel, acc, color, size, delta_size))

    def draw(self, renderer: Renderer):
        for particle in self._particles:
            particle.draw(renderer)

    def update(self, delta_time):
        self._time_passed += delta_time
        self._delay_timer += delta_time

        if self._delay_timer > self.delay_time:
            pos = Vector2(SCREEN_SIZE.x * random(), SCREEN_SIZE.y + 10)
            self.addParticle(pos, self.start_velocity, self.start_acceleration, (255, 255, 255), self.size +
                             Vector2(self.size_range.x * random(), self.size_range.y * random()), delta_size=Vector2(0.0, 0.0))
            self._delay_timer = 0

        removable_particles = []
        for particle in self._particles:
            particle.update(delta_time)
            if particle.position.y < -5:
                removable_particles.append(particle)

        for particle in removable_particles:
            self._particles.remove(particle)
