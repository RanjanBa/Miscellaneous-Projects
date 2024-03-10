from entities.body import BodyType
from entities.dot import Dot
from entities.spring import Spring
from renderer import Renderer
from utilities.colors import BLACK, WHITE


class Entity():
    def __init__(self, dots: list[Dot], fill_color=WHITE, body_type=BodyType.DYNAMIC):
        self.__body_type = body_type
        self._dots = dots
        self._fill_color = fill_color
        self.__springs: list[Spring] = []

        # total_pos = Vector2(0, 0)

        # for dot in dots:
        #     total_pos += dot.position

        # self.__pos = total_pos / len(total_pos)

    @property
    def body_type(self):
        return self.__body_type

    @body_type.setter
    def body_type(self, v):
        self.__body_type = v

    @ property
    def dots(self):
        return self._dots

    def addSpring(self, spring):
        self.__springs.append(spring)

    def draw(self, renderer: Renderer, draw_pt: bool = False):
        if len(self._dots) == 1:
            renderer.renderCircle(
                self._dots[0].position, 5, self._fill_color)
        elif len(self._dots) == 2:
            renderer.renderLine(
                self._dots[0].position, self._dots[1].position, self._fill_color)
        elif len(self._dots) > 2:
            renderer.renderPolygon(
                [dot.position for dot in self._dots], self._fill_color)

        if draw_pt:
            for dot in self._dots:
                dot.draw(renderer)

    def applyConstraints(self, delta_time):
        for sp in self.__springs:
            dir = sp.dotB.position - sp.dotA.position

            dst = dir.length()
            if dst == 0:
                continue

            dir /= dst

            vel_a = sp.dotA.position - sp.dotA.body.old_position
            vel_b = sp.dotB.position - sp.dotB.body.old_position

            rel_vel = vel_b - vel_a

            damp_force = Spring.spring_damping * dir.dot(rel_vel)

            force = Spring.spring_const * (dst - sp.restDst) + damp_force

            force_a = -force * dir
            force_b = force * dir
            
            sp.dotB.body.addForce(force_a)
            sp.dotA.body.addForce(force_b)

    def update(self, delta_time: float):
        for dot in self._dots:
            dot.body.update(delta_time)


class SpecialEntity(Entity):
    def __init__(self, dots: list[Dot], row_divide, column_divide, fill_color=WHITE, body_type=BodyType.DYNAMIC):
        self.__row_divide = row_divide
        self.__column_divide = column_divide
        super().__init__(dots, fill_color, body_type)

    def draw(self, renderer: Renderer, draw_pt: bool = False):
        l = len(self._dots)
        for i in range(0, len(self._dots)):
            r = i / (self.__column_divide + 1)
            c = i % (self.__column_divide + 1)

            if r == self.__row_divide:
                break

            if c == self.__column_divide:
                continue

            points = []
            points.append(self._dots[i].position)
            points.append(self._dots[i+1].position)
            points.append(self._dots[i+1+self.__column_divide + 1].position)
            points.append(self._dots[i+self.__column_divide+1].position)
            renderer.renderPolygon(points, self._fill_color)

            if draw_pt:
                for dot in self._dots:
                    dot.draw(renderer)
