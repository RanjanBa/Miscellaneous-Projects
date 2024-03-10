import random
from pygame import Vector2
from entitites.particle_system import ParticleSystem
from renderer import Renderer
from utilities.colors import BLACK, BLUE


class Bomb:
    def __init__(self, position: Vector2, radius: float, life_time: float = 2, color=BLACK):
        self.__position = position
        self.__radius = radius
        self.__life_time = life_time
        self.__color = color
        self.__timer = 0.0
        self.__is_exploded = False

    @property
    def is_exploded(self):
        return self.__is_exploded
    
    @property
    def life_time(self):
        return self.__life_time
    
    @property
    def life_timer(self):
        return self.__timer

    def explode(self) -> ParticleSystem:
        cnt = 100
        particle_system = ParticleSystem(cnt, 1.5, BLUE)

        rand = random.Random()

        for i in range(cnt):
            dir = Vector2(-1 + rand.random() * 2, -1 + rand.random() * 2)

            if dir.magnitude() != 0:
                dir = dir.normalize()

            particle_system.addParticle(
                Vector2(self.__position.x, self.__position.y), dir * (120 + rand.random() * 40), dir * -1 * (rand.random() * 40 + 60), rand.random() * 5 + 5)

        self.__is_exploded = True
        return particle_system
    
    def update(self, delta_time : float):
        self.__timer += delta_time

    def draw(self, renderer: Renderer):
        renderer.renderCircle(self.__position, self.__radius, self.__color)