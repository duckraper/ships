from math import ceil, pi, sin, cos, radians
from resources import *
from normalshot import NormalShot
from debug import debug

class Ship(pg.sprite.Sprite):
    """Clase que representa una nave en el juego"""

    __ANIMATION_SPEED = 4
    speed: int = calculate_speed(800)
    shot_cd = 200  # shots cooldown(ms)
    MAX_LIFE = 200

    def __init__(self, side: str, position, rotation) -> None:
        """
        Inicializa una nueva instancia de la clase Ship.
        """

        super().__init__()

        self.__alive = True

        self.life: int = self.MAX_LIFE
        self.prev_life: int = self.life
        self.side: str = side

        if pg.joystick.get_count() > 0 and self.side == "left":
            self.joystick = joysticks[0]
        elif pg.joystick.get_count() > 1 and self.side == "right":
            self.joystick = joysticks[1]
        else:
            self.joystick = None

        self.__spritesheet: list[Surface] = spritesheet[f"{self.side}_ship"]

        self.__spritesheet_size: int = len(self.__spritesheet)

        self.moving = True
        self.__current_sprite: int = 0

        self.x, self.y = position

        self.image: Surface = self.__spritesheet[self.__current_sprite]
        self.rect = self.image.get_rect(center=position)
        self.mask = pg.mask.from_surface(self.image)
        
        self.rotation_rate = 4
        self.rotation: int = rotation
        self.radians = radians(self.rotation)

        self.max_ammo = 3.6
        self.shots = pg.sprite.Group()
        self.shot_timer: int = 0
        self.shots_speed = calculate_speed(1000)

        # Manejo de las vibraciones
        # Duración de la vibración (en milisegundos)
        self.vibration_duration = 0
        self.vibration_frequency = 50
        # Amplitud de la vibración (cantidad de píxeles)
        self.vibration_amplitude = 2
        self.vibration_vector = pg.Vector2(0, 0)
        self.vibrate_x = True
        self.vibrate_y = True

    def __input(self, delta):
        key = pg.key.get_pressed()
        rotation = 0

        if self.moving:
            if self.side == "right":
                if key[pg.K_SPACE]:
                    self.shoot()
                
                if key[pg.K_UP] or key[pg.K_w]:
                    dx = self.speed * sin(self.radians)
                    dy = self.speed * cos(self.radians)

                    self.rect.x -= dx * delta
                    self.rect.y -= dy * delta
                
                elif key[pg.K_DOWN] or key[pg.K_s]:
                    dx = (self.speed // 2) * sin(self.radians)
                    dy = (self.speed // 2) * cos(self.radians)

                    self.rect.x += dx * delta
                    self.rect.y += dy * delta

                if key[pg.K_LEFT] or key[pg.K_a]:
                    rotation += self.rotation_rate

                if key[pg.K_RIGHT] or key[pg.K_d]:
                    rotation -= self.rotation_rate
                    
            elif self.side == "left" and self.joystick is not None:
                if self.joystick.get_button(0):
                    self.shoot()
                
                # DEADZONE = -0.0001
                if -1 <= self.joystick.get_axis(1) < -0.0001:
                    dx = self.speed * sin(self.radians)
                    dy = self.speed * cos(self.radians)

                    self.rect.x -= dx * delta
                    self.rect.y -= dy * delta

                elif 0 < self.joystick.get_axis(1) <= 1:
                    dx = (self.speed // 2) * sin(self.radians)
                    dy = (self.speed // 2) * cos(self.radians)

                    self.rect.x += dx * delta
                    self.rect.y += dy * delta

                # TODO: rectificar los triggers
                if self.joystick.get_axis(4) > 0:
                    rotation += self.rotation_rate

                if self.joystick.get_axis(5) > 0:
                    rotation -= self.rotation_rate

        self.rotation += rotation

    def __shake(self, delta) -> None:
        """
        Simula una vibración suave de la nave.
        """
        if self.vibration_duration > 0:
            time_elapsed: int = pg.time.get_ticks()
            displacement: float = self.vibration_amplitude * sin(
                2 * pi * self.vibration_frequency * time_elapsed / 1000
            )

            # Aplica el desplazamiento a la posición vertical de la nave
            if self.vibrate_y:
                self.rect.centery += int(displacement)
            if self.vibrate_x:
                self.rect.centerx += int(displacement)

            # Reduce la duración de la vibración
            self.vibration_duration -= (delta * 1000)
            if self.vibration_duration <= 0:
                # Detiene la vibración al finalizar la duración
                self.vibration_vector = pg.Vector2(0, 0)

    def __constraints(self) -> None:
        """Define las limitantes de cada nave"""
        if self.rect.right >= screen_width:
            self.rect.right = screen_width - 2
        elif self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

        if self.life <= 0:
            self.__alive = False

    def __animate(self, delta) -> None:
        """Metodo quee controla las animaciones de cada accion de las naves"""
        if self.moving:
            self.__current_sprite = (
                self.__current_sprite + self.__ANIMATION_SPEED * delta) % self.__spritesheet_size
        else:
            self.__current_sprite %= self.__spritesheet_size // 2

        self.image = pg.transform.rotate(
            self.__spritesheet[int(self.__current_sprite)], self.rotation)
        
        self.mask = pg.mask.from_surface(self.image)

    def __handle_life_bar(self) -> None:
        """
        Actualiza las barras de vida cuando la vida es modificada
        (Hay curacion o danho)
        """
        pass

    def __draw_life_bar(self) -> None:
        """Dibuja la barra de vida, solo la dibuja, no la actualiza"""
        pass

    def get_damage(self, damage: int) -> None:
        """Calcula el dano recibido y lo actualiza en la vida"""

        damage = ceil(damage)

        if self.life - damage <= 0:
            self.__alive = False

        self.life -= damage

    def get_healing(self, healing) -> None:
        """
        Calcula la vida recibida y lo actualiza
        Args:
            healing: cantidad de vida recibida
        """
        if self.life + healing >= self.MAX_LIFE:
            return

        self.life += healing

    def set_speed(self, speed) -> None:
        """
        Cambia los valores de la velocidad en cierta situacion
        """
        self.speed = speed

    def shoot(self) -> None:
        """Hace que la nave dispare"""
        current_time: int = pg.time.get_ticks()

        if len(self.shots) < self.max_ammo and current_time - self.shot_timer >= self.shot_cd:
            shot = NormalShot(self.side, self.rect.centerx,
                              self.rect.centery, self.shots_speed, self.rotation)

            self.shots.add(shot)
            self.shake(duration=50, amplitude=6,
                       vertical=False, horizontal=True)
            self.shot_timer = current_time

    def shake(self, duration=100, frequency=50, amplitude=2, vertical=True, horizontal=True) -> None:
        """
        Establece el valor de los parametros para que suceda la vibracion
        Args:
            duration: duracion de la vibracion en ms
            frequency: frecuencia con la que oscila
            amplitude: cantidad de px que se desplazara
            vertical: define si la nave va a vibrar de arriba hacia abajo
            horizontal: define si la nave vibrara hacia los lados
        """
        self.vibration_duration: int = duration
        self.vibration_frequency: int = frequency
        self.vibration_amplitude: int = amplitude
        self.vibration_vector = pg.Vector2(0, self.vibration_amplitude)
        self.vibrate_y: bool = vertical
        self.vibrate_x: bool = horizontal

    def update(self, delta) -> None:
        if not self.__alive:
            self.kill()

        if self.alive():
            self.__constraints()
            self.__animate(delta)
            self.__input(delta)
            self.__shake(delta)
            self.__draw_life_bar()

            self.shots.update(delta)
            self.shots.draw(screen)

            if self.prev_life != self.life:
                self.__handle_life_bar()

            # Controlar rotacion
            self.rotation = int(self.rotation)
            self.radians = radians(self.rotation)
            if not -360 < self.rotation < 360:
                self.rotation = 0

            self.prev_life = self.life

        if self.side == "left":
            debug(self.life)
        else:
            debug(self.life, screen_width - 40)
