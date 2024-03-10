from pygame import Vector2

from renderer import Renderer

from entitites.grid import Grid
from entitites.level_generator import levelGenerator
from settings import GRID_SIZE, LINE_WIDTH

from utilities.colors import BLUE, WHITE, YELLOW
from utilities.rect import Rect


class World:
    def __init__(self):
        self.__cell_size = GRID_SIZE
        self.__line_width = LINE_WIDTH

        self.__is_visited: list[list[bool]] = []

        self.food_radius = 5
        self.level_map: list[list[Grid]] = []

    def size(self) -> tuple:
        return (self.__row_cnt, self.__col_cnt)

    def loadLevel(self, level_path: str):
        self.level_map: list[list[Grid]] = levelGenerator(level_path)
        self.__row_cnt = len(self.level_map)
        self.__col_cnt = len(self.level_map[0])

        self.__is_visited = []
        self.__path_map = []
        for i in range(self.__row_cnt):
            row: list[bool] = []
            path: list[tuple(int, int)] = []
            for j in range(self.__col_cnt):
                row.append(False)
                path.append((-1, -1))

            self.__is_visited.append(row)
            self.__path_map.append(path)

    def getPositionAtCoordinate(self, row: int, col: int):
        x_pos = self.__line_width + \
            (self.__cell_size.x + self.__line_width) * \
            col + self.__cell_size.x / 2

        y_pos = self.__line_width + \
            (self.__cell_size.y + self.__line_width) * \
            row + self.__cell_size.y / 2

        return Vector2(x_pos, y_pos)

    def getCoordinate(self, pos: Vector2):
        x_pos = pos.x - self.__line_width - self.__cell_size.x / 2
        col = x_pos // (self.__cell_size.x + self.__line_width)

        y_pos = pos.y - self.__line_width - self.__cell_size.y / 2
        row = y_pos // (self.__cell_size.y + self.__line_width)

        return Vector2(row, col)

    def getShortestPath(self, start_cell: Vector2, target_cell: Vector2):
        for i in range(len(self.__is_visited)):
            for j in range(len(self.__is_visited[i])):
                self.__is_visited[i][j] = False
                self.__path_map[i][j] = (-1, -1)

        queue = [(int(start_cell.x), int(start_cell.y))]

        while len(queue) > 0:
            cur = queue.pop(0)

            if self.__is_visited[cur[0]][cur[1]] == True:
                continue

            self.__is_visited[cur[0]][cur[1]] = True

            if cur[0] == int(target_cell.x) and cur[1] == int(target_cell.y):
                break

            g = self.level_map[cur[0]][cur[1]]
            if g.up == False:
                if self.__is_visited[cur[0] + 1][cur[1]] == False:
                    self.__path_map[cur[0] + 1][cur[1]] = cur
                    queue.append((cur[0] + 1, cur[1]))

            if g.left == False:
                if self.__is_visited[cur[0]][cur[1] - 1] == False:
                    self.__path_map[cur[0]][cur[1] - 1] = cur
                    queue.append((cur[0], cur[1] - 1))

            if g.down == False:
                if self.__is_visited[cur[0] - 1][cur[1]] == False:
                    self.__path_map[cur[0] - 1][cur[1]] = cur
                    queue.append((cur[0] - 1, cur[1]))

            if g.right == False:
                if self.__is_visited[cur[0]][cur[1] + 1] == False:
                    self.__path_map[cur[0]][cur[1] + 1] = cur
                    queue.append((cur[0], cur[1] + 1))

        path = [(int(target_cell.x), int(target_cell.y))]
        while True:
            if path[-1][0] == int(start_cell.x) and path[-1][1] == int(start_cell.y):
                break

            if path[-1][0] == -1 and path[-1][1] == -1:
                return None

            path.append(self.__path_map[path[-1][0]][path[-1][1]])

        return path

    def drawGrid(self, row_idx: int, col_idx: int, renderer: Renderer, color=WHITE):
        pos = self.getPositionAtCoordinate(row_idx, col_idx)

        rect = Rect(pos, GRID_SIZE)

        renderer.renderRect(rect, color)

    def drawPath(self, renderer: Renderer, path: list[tuple]):
        if path is None:
            return

        for p in path:
            self.drawGrid(p[0], p[1], renderer, BLUE)

    def draw(self, renderer: Renderer):
        for i in range(self.__row_cnt):
            for j in range(self.__col_cnt):
                pos = self.getPositionAtCoordinate(i, j)
                g = self.level_map[i][j]

                color = WHITE

                if g.up:
                    x_pos = pos.x
                    y_pos = pos.y + self.__cell_size.y / 2 + self.__line_width / 2
                    center = Vector2(x_pos, y_pos)

                    size = Vector2(self.__cell_size.x +
                                   self.__line_width * 2, self.__line_width)
                    rect = Rect(center, size)
                    renderer.renderRect(rect, color)

                if g.left:
                    x_pos = pos.x - self.__cell_size.x / 2 - self.__line_width / 2
                    y_pos = pos.y
                    center = Vector2(x_pos, y_pos)

                    size = Vector2(self.__line_width,
                                   self.__cell_size.y + self.__line_width * 2)
                    rect = Rect(center, size)
                    renderer.renderRect(rect, color)

                if g.down:
                    x_pos = pos.x
                    y_pos = pos.y - self.__cell_size.y / 2 - self.__line_width / 2
                    center = Vector2(x_pos, y_pos)

                    size = Vector2(self.__cell_size.x +
                                   self.__line_width * 2, self.__line_width)
                    rect = Rect(center, size)
                    renderer.renderRect(rect, color)

                if g.right:
                    x_pos = pos.x + self.__cell_size.x / 2 + self.__line_width / 2
                    y_pos = pos.y
                    center = Vector2(x_pos, y_pos)

                    size = Vector2(self.__line_width,
                                   self.__cell_size.y + self.__line_width * 2)
                    rect = Rect(center, size)
                    renderer.renderRect(rect, WHITE)

                if g.food:
                    renderer.renderCircle(pos, self.food_radius, YELLOW)
