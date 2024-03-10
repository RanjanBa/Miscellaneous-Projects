import pygame as pg

from pygame import Vector2
from utilities.colors import *


class Renderer:
    # __instance = None

    # @staticmethod
    # def getInstance():
    #     if Renderer.__instance == None:
    #         Renderer()
    #     return Renderer.__instance

    # def __init__(self, surface):
    #     if Renderer.__instance != None:
    #         raise Exception('This class is singleton')
    #     else:
    #         Renderer.__instance = self
    #         self.__surface = surface

    def __init__(self, surface):
        self.__surface = surface

    @property
    def surface(self):
        return self.__surface

    def screenSize(self):
        return Vector2(self.__surface.get_size())

    def __convert_coordinate(self, pos) -> Vector2:
        pos = Vector2(pos)
        pos.y = self.screenSize().y - pos.y
        return pos

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

    def renderRect(self, rect, color=WHITE, border_radius=0, alpha=None, border_radii=None):
        pos = self.__convert_coordinate(Vector2(rect.center))
        size = Vector2(rect.size)
        if alpha is None:
            if border_radii is None:
                pg.draw.rect(self.__surface, color, (pos.x - size.x // 2, pos.y -
                                                     size.y // 2, size.x, size.y), border_radius=border_radius)
            else:
                pg.draw.rect(self.__surface, color, (pos.x - size.x // 2, pos.y - size.y // 2, size.x,
                                                     size.y), border_bottom_left_radius=border_radii[0], border_bottom_right_radius=border_radii[1], border_top_right_radius=border_radii[2], border_top_left_radius=border_radii[3])
        else:
            surf = pg.Surface((size.x, size.y))
            surf.set_colorkey((0, 0, 0))
            surf.set_alpha(alpha)
            if border_radii is None:
                pg.draw.rect(surf, color, (0, 0, size.x, size.y),
                             border_radius=border_radius)
            else:
                pg.draw.rect(surf, color, (0, 0, size.x, size.y), border_bottom_left_radius=border_radii[
                             0], border_bottom_right_radius=border_radii[1], border_top_right_radius=border_radii[2], border_top_left_radius=border_radii[3])
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
