"""ARCHIVO DE RECURSOS E IMPORTACIONES PARA EL JUEGO"""
import pygame as pg
import os
import random
from pathlib import Path
from pygame.surface import Surface
from pygame.math import Vector2

pg.display.init()

monitor_size = (pg.display.Info().current_w, pg.display.Info().current_h)
screen_size = (monitor_size[1] - 100, monitor_size[1] - 100)
screen_width, screen_height = screen_size

screen: Surface = pg.display.set_mode(screen_size, pg.NOFRAME)

FPS = 60

SPRITE_SIZE: tuple[int, int] = (screen_width//15, screen_width // 15)
# SPRITE_SIZE = (screen_width//4, screen_width// 4)

# script_directory: str = os.path.dirname(__file__)
script_directory: Path = Path(__file__).resolve().parent

pg.joystick.init()

joy_count = 0
joysticks: list[pg.joystick.JoystickType] = []


def load_image(filepath) -> Surface:
    return pg.image.load(filepath).convert_alpha()


def load_sprites(directory, file_pattern, size=SPRITE_SIZE) -> Surface | list[Surface]:
    sprite_list: list[Surface] = []
    files: int = len(list(script_directory.joinpath(
        "data", "sprites", directory).iterdir()))

    for i in range(files):
        sprite_filepath: Path = script_directory.joinpath(
            "data", "sprites", directory, file_pattern.format(i=i))
        if files == 1:
            return pg.transform.scale(load_image(str(sprite_filepath)), size)
        sprite_list.append(pg.transform.scale(load_image(str(sprite_filepath)), size))

    return sprite_list


spritesheet: dict[str, Surface | list[Surface]] = {
    "left_ship": load_sprites("ships/left", "left_ship-0{i}.png"),
    "right_ship": load_sprites("ships/right", "right_ship-0{i}.png"),
    "little_blast": load_sprites("blasts/little_blast", "little_blast-0{i}.png"),
    "spear_blast": load_sprites("blasts/spear_blast", "spear_blast-0{i}.png"),
    "explosion": load_sprites("extras/explosion", "explosion-0{i}.png"),
    "normal_shot": load_sprites("blasts/normal_shot", "normal_shot-0{i}.png")
}

colors = {
    "black": (18, 22, 25),
    "jasmine": (244, 213, 141),
    "pink": (147, 47, 109),
    "gray": (154, 160, 168),
    "red": (165, 1, 4),
    "white": (250, 250, 250)
}

movement: dict[str, Vector2] = {
    "up": Vector2(0, -1),
    "down": Vector2(0, 1),
    "right": Vector2(1, 0),
    "left": Vector2(-1, 0),
}


def get_font(size: int, font) -> pg.font.Font:
    font = pg.font.Font(os.path.join(
        script_directory, "data", "fonts", font), size)
    return font


def between(value, min, max):
    return min <= value <= max


def get_joystick():
    for event in pg.event.get():
        if event.type == pg.JOYDEVICEADDED:
            joysticks.append(pg.joystick.Joystick(event.device_index))
            joy_count = pg.joystick.get_count()
            print(f"Joystick {event.device_index} connected\n"
                  f"actual joysticks: {joy_count}")


def calculate_speed(base_speed, width=screen_width):
    scale_factor = screen_width // 600
    adaptive_speed = int(base_speed * scale_factor)
    return adaptive_speed


def generate_light_color():
    # Generar valores de color claro
    red_channel = random.randint(180, 255)
    green_channel = random.randint(180, 255)
    blue_channel = random.randint(160, 255)

    # Agregar variabilidad al color para evitar colores demasiado similares
    variation = random.randint(0, 30)
    red_channel = min(255, red_channel + variation)
    green_channel = min(255, green_channel + variation)
    blue_channel = min(255, blue_channel + variation)

    return red_channel, green_channel, blue_channel
