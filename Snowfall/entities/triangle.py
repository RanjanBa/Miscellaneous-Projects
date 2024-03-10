import math
import pymunk
from pygame import Vector2
from pymunk.shapes import Shape
from entities.entity import RigidBody
from renderer import Renderer
from utilities.colors import WHITE


class Trianlge(RigidBody):
    # equilateral triangle
    """
        pos : centroid
        length : distance from centroid to one of the corners
    """

    def __init__(self, pos: Vector2, length: float, angle: float = 0, color=WHITE, body_type=pymunk.Body.DYNAMIC):
        bl = Vector2(-1, 0) * length
        bl.rotate_ip(30)

        br = Vector2(1, 0) * length
        br.rotate_ip(-30)

        tp = Vector2(0, 1) * length
        shape = pymunk.Poly(None, [(bl.x, bl.y), (br.x, br.y), (tp.x, tp.y)])

        super().__init__(pos, angle, shape=shape, color=color, body_type=body_type)
        self.length = length

    def draw(self, renderer: Renderer):
        pos = self.position
        bl = Vector2(-1, 0) * self.length
        bl.rotate_ip(30 + math.degrees(self.angle))

        br = Vector2(1, 0) * self.length
        br.rotate_ip(-30 + math.degrees(self.angle))

        tp = Vector2(0, 1) * self.length
        tp.rotate_ip(math.degrees(self.angle))

        renderer.renderPolygon([bl + pos, br + pos, tp + pos], self.color)
