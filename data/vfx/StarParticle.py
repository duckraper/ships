from data.vfx.Particle import Particle
from random import randint, uniform
from resources import generate_light_color, screen_width, screen_height

class StarParticle(Particle):
    def __init__(self) -> None:
        x = randint(0, screen_width)
        y = randint(0, screen_height)
        color: tuple[int, int, int] = generate_light_color()
        size = randint(1,2)
        speed = randint(1, 40)
        super().__init__(x, y, size, speed, color)