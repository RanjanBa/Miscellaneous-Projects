from pygame import Vector2

from entities.body import Body, BodyType
from renderer import Renderer
from utilities.colors import BLACK


class Dot():
    def __init__(self, pos: Vector2, radius: float = 2, color=BLACK, body_type=BodyType.DYNAMIC):
        self.__body = Body(pos, 1, body_type)
        self.__radius = radius
        self.__color = color

    @property
    def position(self):
        return self.__body.position

    @ property
    def body(self):
        return self.__body

    @ body.setter
    def body(self, v):
        self.__body = v

    @ property
    def radius(self):
        return self.__radius

    @ radius.setter
    def radius(self, v):
        self.__radius = v

    @ property
    def color(self):
        return self.__color

    @ color.setter
    def color(self, v):
        self.__color = v

    def draw(self, renderer: Renderer):
        renderer.renderCircle(self.position, self.radius, self.color)
        
    def update(self, delta_time):
        self.__body.update(delta_time)