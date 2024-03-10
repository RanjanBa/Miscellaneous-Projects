from abc import ABC, abstractmethod

from pygame import Vector2
import pymunk
from renderer import Renderer
from utilities.colors import WHITE


class Entity(ABC):
    def __init__(self, pos: Vector2, angle: float, color=WHITE):
        self.__position = pos
        self.__angle = angle
        self.color = color

    @abstractmethod
    def draw(self, renderer: Renderer):
        pass

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, v):
        self.__position = v

    @property
    def angle(self):
        return self.__angle

    @angle.setter
    def angle(self, v):
        self.__angle = v

class RigidBody(Entity):
    def __init__(self, pos: Vector2, angle: float, shape: pymunk.Shape, color=WHITE, body_type=pymunk.Body.DYNAMIC):
        self.__body = pymunk.Body(body_type=body_type)
        self.__body.position = (pos.x, pos.y)
        self.__body.angle = angle
        self.__shape = shape
        self.__shape.body = self.__body
        super().__init__(pos, angle, color=color)

    @property
    def body(self):
        return self.__body

    @property
    def shape(self):
        return self.__shape
    
    @property
    def position(self):
        return self.__body.position

    @position.setter
    def position(self, v):
        self.__body.position = v

    @property
    def angle(self):
        return self.__body.angle

    @angle.setter
    def angle(self, v):
        self.__body.angle = v
