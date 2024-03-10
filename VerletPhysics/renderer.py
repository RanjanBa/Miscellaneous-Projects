from typing import Dict, Tuple
import pygame as pg

from pygame import Vector2
from utilities.colors import *


class LineGizmo:
    def __init__(self, duration: float, start_pos: Vector2, end_pos: Vector2, color: Tuple[int, int, int], width: int):
        self.duration = duration
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.color = color
        self.width = width


class PointGizmo:
    def __init__(self, duration: float, pos: Vector2, radius: int, color: Tuple[int, int, int]):
        self.duration = duration
        self.position = pos
        self.radius = radius
        self.color = color


class Renderer:
    __instance = None

    @staticmethod
    def getInstance():
        if Renderer.__instance == None:
            Renderer()
        return Renderer.__instance

    def __init__(self, surface):
        if Renderer.__instance != None:
            raise Exception('This class is singleton')
        else:
            Renderer.__instance = self
            self.__surface = surface
            self.__line_gizmos: Dict[int, LineGizmo] = {}
            self.__point_gizmos: Dict[int, PointGizmo] = {}

    # def __init__(self, surface):
    #     self.__surface = surface

    @property
    def surface(self):
        return self.__surface

    @property
    def screenSize(self):
        return Vector2(self.__surface.get_size())

    def __convert_coordinate(self, pos) -> Vector2:
        pos = Vector2(pos)
        pos.y = self.screenSize.y - pos.y
        return pos

    def addLineGizmos(self, line: LineGizmo):
        self.__line_gizmos[line.__hash__()] = line

    def addPointGizmos(self, point: PointGizmo):
        self.__point_gizmos[point.__hash__()] = point

    def renderGizmos(self, delta_time: float):
        removable_gizmos = []
        for key in self.__line_gizmos:
            l = self.__line_gizmos[key]
            self.renderLine(l.start_pos, l.end_pos, l.color, l.width)
            
            l.duration -= delta_time
            if l.duration <= 0:
                removable_gizmos.append(key)

        for key in removable_gizmos:
            self.__line_gizmos.pop(key)

        removable_gizmos = []
        for key in self.__point_gizmos:
            p = self.__point_gizmos[key]
            self.renderCircle(p.position, p.radius, p.color)
            
            p.duration -= delta_time
            if p.duration <= 0:
                removable_gizmos.append(key)
        
        for key in removable_gizmos:
            self.__point_gizmos.pop(key)

    def renderText(self, label, pos, font_size=24, color=GREEN):
        pos = self.__convert_coordinate(pos)
        font = pg.font.SysFont("comicsansms", font_size)
        text_renderer = font.render(label, True, color)
        self.__surface.blit(text_renderer, (pos.x - text_renderer.get_width() //
                                            2, pos.y - text_renderer.get_height() // 2))

    def renderLine(self, start, end, color=WHITE, weight=1):
        start = self.__convert_coordinate(start)
        end = self.__convert_coordinate(end)
        pg.draw.line(self.__surface, color,
                     (start.x, start.y), (end.x, end.y), weight)

    def renderWireRect(self, rect, color=WHITE, weight=1):
        pos = self.__convert_coordinate(Vector2(rect.center))
        size = Vector2(rect.size)
        ul = Vector2(pos.x - size.x//2, pos.y - size.y // 2)
        ur = Vector2(pos.x + size.x//2, pos.y - size.y // 2)
        bl = Vector2(pos.x - size.x//2, pos.y + size.y // 2)
        br = Vector2(pos.x + size.x//2, pos.y + size.y // 2)
        self.renderLine(Vector2(ul.x, ul.y), Vector2(
            ur.x, ur.y), color, weight)
        self.renderLine(Vector2(ur.x, ur.y), Vector2(
            br.x, br.y), color, weight)
        self.renderLine(Vector2(br.x, br.y), Vector2(
            bl.x, bl.y), color, weight)
        self.renderLine(Vector2(bl.x, bl.y), Vector2(
            ul.x, ul.y), color, weight)

    def renderRect(self, rect, color=WHITE, alpha=None):
        pos = self.__convert_coordinate(Vector2(rect.center))
        size = Vector2(rect.size)
        if alpha is None:
            pg.draw.rect(self.__surface, color, (pos.x -
                                                 size.x // 2, pos.y - size.y // 2, size.x, size.y))
        else:
            surf = pg.Surface((size.x, size.y))
            surf.set_colorkey((0, 0, 0))
            surf.set_alpha(alpha)
            pg.draw.rect(surf, color, (0, 0, size.x, size.y))
            self.__surface.blit(
                surf, (pos.x - size.x // 2, pos.y - size.y // 2))

    def renderCircle(self, pos, radius, color=WHITE, alpha=None, width=0):
        pos = self.__convert_coordinate(pos)
        if alpha is None:
            pg.draw.circle(self.__surface, color,
                           (pos.x, pos.y), radius, width)
        else:
            surf = pg.Surface((2 * radius, 2 * radius))
            surf.set_colorkey((0, 0, 0))
            surf.set_alpha(alpha)
            pg.draw.circle(surf, color, (radius, radius), radius, width)
            self.__surface.blit(surf, (pos.x - radius, pos.y - radius))

    def renderPolygon(self, points, color=WHITE, alpha=None):
        points = [self.__convert_coordinate(pt) for pt in points]
        if len(points) <= 0:
            raise Exception('polygon doesn\'t contain any point.')
        if alpha is None:
            pg.draw.polygon(self.surface, color, [
                            (pt.x, pt.y) for pt in points])
        else:
            min_x = points[0].x
            min_y = points[0].y
            max_x = points[0].x
            max_y = points[0].y

            for pt in points:
                if pt.x < min_x:
                    min_x = pt.x

                if pt.y < min_y:
                    min_y = pt.y

                if pt.x > max_x:
                    max_x = pt.x

                if pt.y > max_y:
                    max_y = pt.y

            surf = pg.Surface((max_x-min_x, max_y - min_y))
            surf.set_colorkey((0, 0, 0))
            surf.set_alpha(alpha)
            pg.draw.polygon(
                surf, color, [(pt.x - min_x, pt.y - min_y) for pt in points])
            self.__surface.blit(surf, (min_x, min_y))
