import sys
import pygame as pg
from renderer import Renderer
from settings import *
from game import *

# for importing files from subfolders
sys.path.append('../')

is_application_running = True


def initilizeScreen():
    pg.init()
    mixer.init()

    display_surface = pg.display.set_mode(
        (int(INITIALIZE_SCREEN_SIZE.x), int(INITIALIZE_SCREEN_SIZE.y)), pg.NOFRAME)
    pg.display.set_caption(TITLE)
    Renderer(display_surface)


def handleApplicationEvents(events):
    for event in events:
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            global is_application_running
            is_application_running = False


def showApplicationScreen():
    clock = pg.time.Clock()
    g = Game()
    while is_application_running:
        delta_time = clock.tick(60)/1000.0
        events = pg.event.get()
        handleApplicationEvents(events)
        g.update(events, delta_time)
        pg.display.update()

    del g


def main():
    initilizeScreen()
    while is_application_running:
        showApplicationScreen()


if __name__ == '__main__':
    main()
