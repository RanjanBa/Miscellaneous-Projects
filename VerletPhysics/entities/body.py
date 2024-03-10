from enum import Enum
from pygame import Vector2


class BodyType(Enum):
    DYNAMIC = 1
    KINEMATIC = 2
    STATIC = 3


class Body():
    def __init__(self, position: Vector2, mass=1, body_type=BodyType.DYNAMIC):
        self.__position = position
        self.__old_position = Vector2(position.x, position.y)
        self.__force = Vector2(0, 0)
        if body_type == BodyType.STATIC:
            self.__mass = 0
        else:
            self.__mass = mass

        self.__inverse_mass = 0
        if self.__mass != 0:
            self.__inverse_mass = 1 / self.__mass

        self.body_type = body_type

    def update(self, delta_time):
        if self.body_type == BodyType.STATIC or self.body_type == BodyType.KINEMATIC:
            return

        acceleration = self.__force * self.__inverse_mass
        if self.__mass != 0:
            acceleration = self.__force / self.__mass

        velocity = self.__position - self.__old_position
        self.__old_position = Vector2(self.__position.x, self.__position.y)

        self.__position += (velocity +
                            acceleration * delta_time * delta_time)

        self.__force = Vector2(0, 0)

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, pos):
        self.__position = pos

    @property
    def old_position(self):
        return self.__old_position

    @old_position.setter
    def old_position(self, pos):
        self.__old_position = pos

    @property
    def mass(self):
        return self.__mass

    @mass.setter
    def mass(self, v):
        self.__mass = v

        self.__inverse_mass = 0

        if self.__mass != 0:
            self.__inverse_mass = 1 / self.__mass

        if self.body_type == BodyType.STATIC:
            self.__mass = 0
            self.__inverse_mass = 0

    @property
    def inverse_mass(self):
        return self.__inverse_mass

    def addForce(self, force: Vector2):
        self.__force += force
