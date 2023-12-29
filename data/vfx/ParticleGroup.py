import resources


class ParticleGroup:
    def __init__(self, num_particles, particle_class):
        self.particles = [particle_class() for _ in range(num_particles)]

    def update(self, delta):
        for particle in self.particles:
            particle.move(delta)

    def draw(self, screen=resources.screen):
        for particle in self.particles:
            particle.draw(screen)
