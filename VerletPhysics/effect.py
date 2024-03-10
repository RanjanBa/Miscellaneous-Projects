from pygame import Vector2
from abc import ABC, abstractmethod
from renderer import Renderer
from utilities.colors import WHITE


class Effect(ABC):
    def __init__(self, pos, life_time=5):
        self.position = Vector2(pos)
        self.life_time = life_time
        self.timer = 0

    @abstractmethod
    def draw():
        pass


class CircleEffect(Effect):
    def __init__(self, pos, radius: int, width: int, life_time=5, color=WHITE):
        super().__init__(pos, life_time)
        self.radius = radius
        self.width = width
        self.color = color
        self.alpha = 255

    def draw(self, delta_time, renderer: Renderer):
        if self.width <= 0:
            return
        renderer.renderCircle(self.position, self.radius,
                              self.color, alpha=self.alpha, width=self.width)
        self.position += Vector2(0, 2)
        self.timer += delta_time
        self.alpha -= 20
        self.alpha = max(0, self.alpha)
        self.radius += 2
        self.width -= 1
