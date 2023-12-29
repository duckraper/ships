from resources import screen_size
import random as r
from pygame import draw

class Particle:
    def __init__(self, x, y, size, speed, color) -> None:
        self.x: int = x
        self.y: int = y
        self.speed: int = speed
        self.size: int = size
        self.color = color

    def move(self, delta):
        self.x -= self.speed * delta
        if self.x < 0:
            self.reset_position()

    def reset_position(self):
        self.x = screen_size[0]
        self.y = r.randint(0, screen_size[1])

    def draw(self, screen):
        draw.circle(screen, self.color, (self.x, self.y), self.size)
    