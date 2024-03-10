from enum import Enum
from pygame import Vector2
from entitites.character import Character
from entitites.world import World
from renderer import Renderer
from utilities.colors import RED


class Enemy(Character):
    class State(Enum):
        IDLE = 0,
        CHASE = 1,
        PATROL = 2
    
    def __init__(self, world: World, pos: Vector2, speed: float, radius: float, color=RED):
        super(Enemy, self).__init__(world, pos, speed)
        self.radius = radius
        self.color = color
        self.__target_player: Character = None
        # self.__path = None
        self.__state : Enemy.State = Enemy.State.IDLE
        self.__patrol_points : list[Vector2] = []
        self.__idle_duration = 2.0
        self.__idle_timer = 0.0
        self.__lastSeenGrid = None

    def _canChase(self, path) -> bool:
        idx = len(path) - 2
        
        while idx >= 0:
            idx -= 1
        
        return False

    def targetPlayer(self, player: Character):
        self.__target_player = player

    def update(self, delta_time: float):
        current_cell = self._world.getCoordinate(self.position)
        current_cell_pos = self._world.getPositionAtCoordinate(
            current_cell.x, current_cell.y)

        player_cell = self._world.getCoordinate(self.__target_player.position)
        
        path = self._world.getShortestPath(current_cell, player_cell)

        self.desired_dir = Character.MoveDirection.NONE

        if path is not None and len(path) > 1:
            if path[-1][0] == path[-2][0]:
                if path[-1][1] < path[-2][1]:
                    self.desired_dir = Character.MoveDirection.RIGHT
                else:
                    self.desired_dir = Character.MoveDirection.LEFT
            elif path[-1][1] == path[-2][1]:
                if path[-1][0] < path[-2][0]:
                    self.desired_dir = Character.MoveDirection.UP
                else:
                    self.desired_dir = Character.MoveDirection.DOWN

        # print(self.desired_dir)

        if self.move_dir == Character.MoveDirection.NONE:
            self.move_dir = self.desired_dir
        elif self.move_dir == Character.MoveDirection.UP and self.desired_dir == Character.MoveDirection.DOWN:
            self.move_dir = self.desired_dir
        elif self.move_dir == Character.MoveDirection.DOWN and self.desired_dir == Character.MoveDirection.UP:
            self.move_dir = self.desired_dir
        elif self.move_dir == Character.MoveDirection.LEFT and self.desired_dir == Character.MoveDirection.RIGHT:
            self.move_dir = self.desired_dir
        elif self.move_dir == Character.MoveDirection.RIGHT and self.desired_dir == Character.MoveDirection.LEFT:
            self.move_dir = self.desired_dir

        if self.move_dir == Character.MoveDirection.UP:
            if self.position.y > current_cell_pos.y:
                current_cell.x += 1
        elif self.move_dir == Character.MoveDirection.DOWN:
            if self.position.y < current_cell_pos.y:
                current_cell.x -= 1
        elif self.move_dir == Character.MoveDirection.LEFT:
            if self.position.x < current_cell_pos.x:
                current_cell.y -= 1
        elif self.move_dir == Character.MoveDirection.RIGHT:
            if self.position.x > current_cell_pos.x:
                current_cell.y += 1

        self.target_cell = self._findTargetCell(
            current_cell, self.move_dir, self.desired_dir)

        target_pos = self._world.getPositionAtCoordinate(
            self.target_cell.x, self.target_cell.y)

        dist_to_target = self.position.distance_to(target_pos)

        dist = self.speed * delta_time

        if dist > dist_to_target:
            dist = dist_to_target

        dir = self._getMoveDirection()

        next_pos = self.position + dist * dir

        self.position = next_pos
        if dist_to_target == 0:
            self.move_dir = Character.MoveDirection.NONE

    def draw(self, renderer: Renderer):
        # self._world.drawPath(renderer, self.__path)
        renderer.renderCircle(self.position, self.radius, self.color)
