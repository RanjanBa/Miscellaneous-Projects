from pygame import Vector2
from renderer import Renderer

from utilities.colors import WHITE


class Particle:
    def __init__(self, radius : float, life_time : float, position : Vector2, velocity : Vector2, acceleration : Vector2, color = WHITE, alpha : int = 100):
        self.__radius = radius
        self.__life_time = life_time
        self.__position = position
        self.__velocity = velocity
        self.__acceleration = acceleration
        self.__color = color
        self.__alpha = alpha
        self.__life_timer = 0
        self.speed_of_radius_fall = 0
    
    @property
    def radius(self):
        return self.__radius
        
    @property
    def lifeTime(self):
        return self.__life_time
    
    @property
    def lifeTimer(self):
        return self.__life_timer
    
    def update(self, delta_time : float):
        self.__life_timer += delta_time
        self.__velocity += self.__acceleration * delta_time
        self.__position += self.__velocity * delta_time
        self.__radius -= delta_time * self.speed_of_radius_fall
    
    def draw(self, renderer : Renderer):
        renderer.renderCircle(self.__position, self.__radius, self.__color, self.__alpha)
        