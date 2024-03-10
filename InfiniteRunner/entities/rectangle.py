import pymunk
from pygame import Rect, Vector2
from entities.entity import RigidBody
from renderer import Renderer
from utilities.colors import WHITE


class Rectangle(RigidBody):
    def __init__(self, rect: Rect, angle: float = 0, color=WHITE, body_type=pymunk.Body.DYNAMIC):
        self.__rect = rect
        shape = pymunk.Poly.create_box(None, rect.size)
        super().__init__(Vector2(rect.center), angle, shape, color=color, body_type=body_type)

    @property
    def size(self) -> Vector2:
        return Vector2(self.__rect.size)

    def draw(self, renderer: Renderer):
        pos = self.position
        
        right = Vector2(1, 0) * self.__rect.size[0] / 2.0
        up = Vector2(0, 1) * self.__rect.size[1] / 2.0

        right.rotate_ip_rad(self.angle)
        up.rotate_ip_rad(self.angle)

        bl = pos - right - up
        tl = pos - right + up
        br = pos + right - up
        tr = pos + right + up
        renderer.renderPolygon([bl, br, tr, tl], self.color)
