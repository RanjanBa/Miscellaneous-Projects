from renderer import Renderer


class GizmosDrawer():
    def __init__(self, renderer: Renderer):
        self.__renderer = renderer
        self.__line_gizmoses = []
        self.__rect_gizmoses = []
        self.__circle_gizmoses = []
