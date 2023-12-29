from blast import Blast, SPRITE_SIZE, spritesheet, screen_width, screen_height
from pygame.transform import scale, rotate
from pygame.mask import from_surface


class NormalShot(Blast):
    def __init__(self, side, x, y, speed, rotation, damage=25, size=(
            (SPRITE_SIZE[0] // 5), SPRITE_SIZE[1] // 5)) -> None:
        super().__init__(side, x, y, speed, rotation, damage, size)

        self.image = scale(spritesheet["normal_shot"], self.size)
        self.mask = from_surface(self.image)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, delta) -> None:
        return super().update(delta)