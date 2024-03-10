from pygame import Vector2
from entitites.particle import Particle
from renderer import Renderer
from utilities.colors import WHITE


class ParticleSystem:
    def __init__(self, max_count: int = 10, life_time: float = 10.0, color=WHITE):
        self.__max_count = max_count
        self.__life_time = life_time
        self.__color = color

        self.__particles: list[Particle] = []
        self.__timer = 0

    @property
    def lifeTime(self):
        return self.__life_time

    @property
    def particleCount(self) -> int:
        return len(self.__particles)

    @property
    def particles(self):
        return self.__particles

    def addParticle(self, pos: Vector2, velocity: Vector2, acceleration: Vector2, radius: float, color=None):
        if self.particleCount == self.__max_count:
            return

        par_color = self.__color if color is None else color
        particle = Particle(radius, self.__life_time, pos, velocity, acceleration, par_color)
        particle.speed_of_radius_fall = 1.0
        self.__particles.append(particle)

    def removeParticle(self, particle):
        if self.__particles.__contains__(particle):
            self.__particles.remove(particle)

    def destroy(self):
        self.__particles = []

    def update(self, delta_time):
        self.__timer += delta_time
        removable_particles = []

        for p in self.__particles:
            if p.lifeTimer > p.lifeTime or p.radius < 3:
                removable_particles.append(p)
                continue

            p.update(delta_time)

        for p in removable_particles:
            self.removeParticle(p)

    def draw(self, renderer: Renderer):
        for p in self.__particles:
            p.draw(renderer)
