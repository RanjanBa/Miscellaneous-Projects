import json
from pygame import Vector2

TITLE = 'SNOW FALL'
FPS = 30
SAVE_DATA_FILE = 'dat/save.json'
BUTTON_SIZE = Vector2(100, 30)
SCREEN_SIZE = Vector2(1350, 760)
VOLUME = 1
SCREEN_SIZES = [(1350, 760), (1200, 700), (1000, 600), (800, 500)]


def save_data(screen_size: Vector2, volume):
    json_object = json.dumps(
        {'screen-size': (int(screen_size.x), int(screen_size.y)), 'volume': volume})

    with open(SAVE_DATA_FILE, "w") as outfile:
        global VOLUME
        VOLUME = volume
        outfile.write(json_object)
        
def load_data():
    f = open(SAVE_DATA_FILE)
    data = json.load(f)
    global SCREEN_SIZE
    SCREEN_SIZE = Vector2(data["screen-size"][0], data["screen-size"][1])
    global VOLUME
    VOLUME = data['volume']
