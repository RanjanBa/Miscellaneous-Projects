import sys
import pygame as pg

import settings

from renderer import Renderer
from game import *

# for importing files from subfolders
sys.path.append('../')

display_surface = None
renderer = None
is_application_running = True


def initilizeScreen():
    pg.init()
    mixer.init()
    global display_surface
    display_surface = pg.display.set_mode(
        (int(settings.SCREEN_SIZE.x), int(settings.SCREEN_SIZE.y)), pg.NOFRAME)
    pg.display.set_caption(settings.TITLE)
    global renderer
    renderer = Renderer(display_surface)


def handleApplicationEvents(events):
    for event in events:
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            global is_application_running
            is_application_running = False


def showApplicationScreen():
    clock = pg.time.Clock()
    g = Game(renderer)
    while is_application_running:
        events = pg.event.get()
        handleApplicationEvents(events)
        g.update(events)
        pg.display.update()
        clock.tick(60)

    del g


def main():
    settings.load_data()
    print(settings.SCREEN_SIZE)
    print(settings.VOLUME)
    initilizeScreen()
    while is_application_running:
        showApplicationScreen()


if __name__ == '__main__':
    main()
