from pygame import Vector2
import pymunk
from entities.entity import RigidBody

from renderer import Renderer
from utilities.colors import WHITE


class Circle(RigidBody):
    def __init__(self, pos: Vector2, radius: float, angle = 0, color=WHITE, body_type=pymunk.Body.DYNAMIC):
        shape = pymunk.Circle(None, radius)
        super().__init__(pos, 0, shape, color=color, body_type=body_type)
        self.radius = radius

    def draw(self, renderer: Renderer):
        renderer.renderCircle(self.position, self.radius, self.color)
