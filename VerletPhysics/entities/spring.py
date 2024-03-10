from entities.dot import Dot


class Spring():
    spring_const = 500.0
    spring_damping = 0.01

    def __init__(self, dotA: Dot, dotB: Dot, spring_const=100, damping_const=0.5):
        self.dotA = dotA
        self.dotB = dotB
        self.spring_const = spring_const
        self.damping_const = damping_const
        self.__restDst = dotA.position.distance_to(dotB.position)

    @property
    def restDst(self):
        return self.__restDst

    def solveConstraints(self):
        pass
