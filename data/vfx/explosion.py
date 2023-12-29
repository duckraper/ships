import pygame as pg
from resources import spritesheet as ss


class Explosion:
    def __init__(self, x, y, size) -> None:
        self.position = (x, y)
        self.size = size
        self.spritesheet = ss["explosion"]
        self.spritesheet_size = len(self.spritesheet)
        self.actual_frame = 0

    def animate(self):
        pass
