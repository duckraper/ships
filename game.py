import pygame.sprite

from time import time
from resources import *
from ship import Ship


class Game:
    def __init__(self) -> None:
        self.running = True
        self.__paused = False

        self.fullscreen = False

        get_joystick()

        pg.display.set_caption("ships project")
        # pg.display.set_icon() # TODO: ponerle icono al juego

        offset = 150

        left_ship = Ship("left", (offset, screen_height // 2))
        right_ship = Ship("right", (screen_width - offset, screen_height // 2))

        
        self.ships = pg.sprite.Group(left_ship, right_ship)

        self.left_ship = pg.sprite.GroupSingle(left_ship)
        self.right_ship = pg.sprite.GroupSingle(right_ship)

        self.bullets = pg.sprite.Group()

        # control del flujo de tiempo
        self.elapsed_time = time()
        self.delta = time() - self.elapsed_time

    # TODO: optimizar colisiones para que solo se compruebe
    #       cuando existan posibilidad de colisiones entre los sprites
    def __handle_collisions(self) -> None:
        """
        Controla las posiciones de los sprites para asi
        controlar si existio collision entre ellos y poder hacer algo
        al respecto si sucede
        """
        left_collided_shots = pg.sprite.spritecollide(sprite=self.left_ship.sprite,
                                                          group=self.right_ship.sprite.shots,
                                                          dokill=False, collided=pg.sprite.collide_mask)
        if left_collided_shots:
            self.left_ship.sprite.get_damage(sum(shot.damage for shot in left_collided_shots))
            self.left_ship.sprite.shake(vertical=True, horizontal=True)
            for shot in left_collided_shots:
                shot.kill()

        right_collided_shots = pg.sprite.spritecollide(sprite=self.right_ship.sprite,
                                                           group=self.left_ship.sprite.shots,
                                                           dokill=True, collided=pg.sprite.collide_mask)
        if right_collided_shots:
            self.right_ship.sprite.get_damage(sum(shot.damage for shot in right_collided_shots))
            self.right_ship.sprite.shake(vertical=True, horizontal=True)
            for shot in right_collided_shots:
                shot.kill()

        # collision de los disparos entre si
        pg.sprite.groupcollide(self.left_ship.sprite.shots, self.right_ship.sprite.shots,
                                   dokilla=True, dokillb=True, collided=pg.sprite.collide_mask)

        # collision de las naves entre si
        if pg.sprite.groupcollide(self.left_ship, self.right_ship, False, False,
                                      collided=pg.sprite.collide_mask):
            """
            las naves al chocar vibraran, quitandose vida, ambas y reduciendo su velocidad
            de movimiento, haciendo asi, que ambas tengan que evitar collisionarse
            """
            collision_damage = 0.5
            for ship in self.ships:
                ship.get_damage(collision_damage)
                ship.set_speed(int(Ship.speed * 0.2))
                ship.shake(amplitude=10)

        else:
            for ship in self.ships:
                ship.set_speed(int(Ship.speed))

    def __update(self) -> None:
        self.delta: float = time() - self.elapsed_time
        self.elapsed_time: float = time()

    def toggle_pause(self) -> None:
        """Invierte el estado de pausado del juego"""
        self.__paused = not self.__paused

    def run(self) -> None:
        screen.fill(color['black'])

        if not self.__paused:
            self.ships.update(self.delta)
            if len(self.ships.sprites()) >= 2:
                self.__handle_collisions()

        self.ships.draw(screen)

        self.__update()
