import math
import random
from pygame import Vector2

from entities.entity import BodyType, Entity
from renderer import LineGizmo, PointGizmo, Renderer
from utilities.collision_detection import findClosestPointOnPolygon, isPointInsidePolygon
from utilities.colors import BLACK, BLUE, RED, YELLOW


class Physics:
    iteration = 1

    def __init__(self, gravity: Vector2 = Vector2(0, -10)):
        self.__entities: list[Entity] = []
        self.__gravity = gravity

    @property
    def gravity(self):
        return self.__gravity

    @gravity.setter
    def gravity(self, v):
        self.__gravity = v

    def addEntity(self, entity: Entity):
        self.__entities.append(entity)

    def applyGravity(self):
        for ent in self.__entities:
            for dot in ent.dots:
                dot.body.addForce(self.gravity)

    def applyConstraints(self, delta_time):
        for ent in self.__entities:
            ent.applyConstraints(delta_time)

    def collisionResolver(self, delta_time):
        for ent1 in self.__entities:
            if ent1.body_type == BodyType.STATIC:
                continue
            for ent2 in self.__entities:
                if ent1 == ent2:
                    continue

                points = [pt.position for pt in ent2.dots]

                for dot in ent1.dots:
                    if isPointInsidePolygon(points, dot.position):
                        pt, line_idx = findClosestPointOnPolygon(
                            points, dot.position)

                        normal = pt - dot.position

                        dst = normal.length()

                        if dst != 0:
                            normal.normalize_ip()

                        dot.body.position = dot.body.position + normal * dst

                        # velA = dot.position - dot.body.old_position
                        # velB = (ent2.dots[line_idx[0]].position - ent2.dots[line_idx[0]].body.old_position) \
                        #     + (ent2.dots[line_idx[1]].position -
                        #        ent2.dots[line_idx[1]].body.old_position)
                        # velB /= 2.0

                        # vel_AB = velB - velA

                        # # Renderer.getInstance().addLineGizmos(LineGizmo(10.0, pt,
                        # #                                                pt + vel_AB, BLUE, 3))

                        # vel_along_normal = vel_AB.dot(normal)

                        # e = 1.0

                        # combine_avg_inverse_mass = (ent2.dots[line_idx[0]].body.inverse_mass +
                        #                             ent2.dots[line_idx[1]].body.inverse_mass) / 2.0

                        # j = -(1+e) * vel_along_normal
                        # j /= (dot.body.inverse_mass + combine_avg_inverse_mass)

                        # impluse = j * normal

                        # velA -= dot.body.inverse_mass * impluse
                        # velB += combine_avg_inverse_mass * impluse
                        # # reflect = 2 * vel.dot(normal) * normal - vel

                        # dot.body.old_position = dot.body.position - velA

                        # Renderer.getInstance().addLineGizmos(LineGizmo(10.0, dot.body.old_position,
                        #                                                dot.body.old_position + normal * 10, RED, 3))
                        # Renderer.getInstance().addPointGizmos(PointGizmo(10.0, pt, 5, BLUE))
                        # Renderer.getInstance().addLineGizmos(
                        #     LineGizmo(10.0, pt, dot.body.position, YELLOW, 3))

    def updatePosition(self, delta_time):
        for ent in self.__entities:
            ent.update(delta_time)

    def step(self, delta_time: float):
        delta_time = delta_time / Physics.iteration

        for i in range(0, Physics.iteration):
            self.applyConstraints(delta_time)
            self.applyGravity()
            self.updatePosition(delta_time)
            self.collisionResolver(delta_time)
