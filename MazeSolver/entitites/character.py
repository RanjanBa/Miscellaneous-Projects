from abc import abstractmethod
from enum import Enum
from pygame import Vector2
from entitites.world import World

from renderer import Renderer


class Character:
    class MoveDirection(Enum):
        NONE = 0,
        UP = 1,
        LEFT = 2,
        DOWN = 3,
        RIGHT = 4

    def __init__(self, world: World, pos: Vector2, speed: float):
        self._world = world
        self.position = pos
        self.speed = speed
        self.move_dir: Character.MoveDirection = Character.MoveDirection.NONE
        self.desired_dir: Character.MoveDirection = Character.MoveDirection.NONE
        self.target_cell: Vector2 = Vector2(-1, -1)

    def _getMoveDirection(self):
        if self.target_cell.x == -1 or self.target_cell.y == - 1:
            return Vector2(0, 0)
        if self.move_dir == self.MoveDirection.UP:
            return Vector2(0, 1)
        if self.move_dir == self.MoveDirection.LEFT:
            return Vector2(-1, 0)
        if self.move_dir == self.MoveDirection.DOWN:
            return Vector2(0, -1)
        if self.move_dir == self.MoveDirection.RIGHT:
            return Vector2(1, 0)

        return Vector2(0, 0)

    def _findTargetCell(self, current_cell: Vector2, move_dir: MoveDirection, desired_dir: MoveDirection):
        while True:
            g = self._world.level_map[int(current_cell.x)][int(current_cell.y)]
            if move_dir == Character.MoveDirection.UP:
                if desired_dir == Character.MoveDirection.UP:
                    if g.up == False:
                        current_cell.x += 1
                    else:
                        break
                elif desired_dir == Character.MoveDirection.LEFT:
                    if g.left == True and g.up == False:
                        current_cell.x += 1
                    else:
                        break
                elif desired_dir == Character.MoveDirection.DOWN:
                    if g.down == False:
                        current_cell.x -= 1
                    else:
                        break
                elif desired_dir == Character.MoveDirection.RIGHT:
                    if g.right == True and g.down == False:
                        current_cell.x += 1
                    else:
                        break
                else:
                    if g.up == False:
                        current_cell.x += 1
                    else:
                        break
            elif move_dir == Character.MoveDirection.LEFT:
                if desired_dir == Character.MoveDirection.UP:
                    if g.up == True and g.left == False:
                        current_cell.y -= 1
                    else:
                        break
                elif desired_dir == Character.MoveDirection.LEFT:
                    if g.left == False:
                        current_cell.y -= 1
                    else:
                        break
                elif desired_dir == Character.MoveDirection.DOWN:
                    if g.down == True and g.left == False:
                        current_cell.y -= 1
                    else:
                        break
                elif desired_dir == Character.MoveDirection.RIGHT:
                    if g.right == False:
                        current_cell.y += 1
                    else:
                        break
                else:
                    if g.left == False:
                        current_cell.y -= 1
                    else:
                        break
            elif move_dir == Character.MoveDirection.DOWN:
                if desired_dir == Character.MoveDirection.UP:
                    if g.up == False:
                        current_cell.x += 1
                    else:
                        break
                elif desired_dir == Character.MoveDirection.LEFT:
                    if g.left == True and g.down == False:
                        current_cell.x -= 1
                    else:
                        break
                elif desired_dir == Character.MoveDirection.DOWN:
                    if g.down == False:
                        current_cell.x -= 1
                    else:
                        break
                elif desired_dir == Character.MoveDirection.RIGHT:
                    if g.right == True and g.down == False:
                        current_cell.x -= 1
                    else:
                        break
                else:
                    if g.down == False:
                        current_cell.x -= 1
                    else:
                        break
            elif move_dir == Character.MoveDirection.RIGHT:
                if desired_dir == Character.MoveDirection.UP:
                    if g.up == True and g.right == False:
                        current_cell.y += 1
                    else:
                        break
                elif desired_dir == Character.MoveDirection.LEFT:
                    if g.left == False:
                        current_cell.y -= 1
                    else:
                        break
                elif desired_dir == Character.MoveDirection.DOWN:
                    if g.down == True and g.right == False:
                        current_cell.y += 1
                    else:
                        break
                elif desired_dir == Character.MoveDirection.RIGHT:
                    if g.right == False:
                        current_cell.y += 1
                    else:
                        break
                else:
                    if g.right == False:
                        current_cell.y += 1
                    else:
                        break
            else:
                if desired_dir == Character.MoveDirection.UP:
                    if g.up == False:
                        current_cell.x += 1
                    else:
                        break
                elif desired_dir == Character.MoveDirection.LEFT:
                    if g.left == False:
                        current_cell.y -= 1
                    else:
                        break
                elif desired_dir == Character.MoveDirection.DOWN:
                    if g.down == False:
                        current_cell.x -= 1
                    else:
                        break
                elif desired_dir == Character.MoveDirection.RIGHT:
                    if g.right == False:
                        current_cell.y += 1
                    else:
                        break
                else:
                    break

        return current_cell

    def update(self, delta_time: float):
        pass

    @abstractmethod
    def draw(self, renderer: Renderer):
        pass
