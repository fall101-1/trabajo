import pygame
import random
import math

# Inicializar pygame
pygame.init()

# Constantes
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()

# Clases
class Ship:
    def __init__(self):
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, WHITE, [(15, 0), (0, 30), (30, 30)])
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.angle = 0
        self.speed = 0
        self.vel = pygame.Vector2(0, 0)

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.angle += 5
        if keys[pygame.K_RIGHT]:
            self.angle -= 5
        if keys[pygame.K_UP]:
            angle_rad = math.radians(self.angle)
            force = pygame.Vector2(math.sin(angle_rad), math.cos(angle_rad)) * -0.2
            self.vel += force

        self.rect.center += self.vel
        self.rect.centerx %= WIDTH
        self.rect.centery %= HEIGHT

    def draw(self, surface):
        rotated = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated.get_rect(center=self.rect.center)
        surface.blit(rotated, new_rect)

    def shoot(self):
        angle_rad = math.radians(self.angle)
        direction = pygame.Vector2(math.sin(angle_rad), math.cos(angle_rad)) * -8
        return Bullet(self.rect.center, direction)

class Bullet:
    def __init__(self, pos, velocity):
        self.pos = pygame.Vector2(pos)
        self.vel = velocity
        self.radius = 3

    def update(self):
        self.pos += self.vel

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.pos.x), int(self.pos.y)), self.radius)

    def off_screen(self):
        return (self.pos.x < 0 or self.pos.x > WIDTH or
                self.pos.y < 0 or self.pos.y > HEIGHT)

class Asteroid:
    def __init__(self):
        self.pos = pygame.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.vel = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.radius = random.randint(20, 40)

    def update(self):
        self.pos += self.vel
        self.pos.x %= WIDTH
        self.pos.y %= HEIGHT

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.pos.x), int(self.pos.y)), self.radius)

# Inicialización
ship = Ship()
bullets = []
asteroids = [Asteroid() for _ in range(5)]
running = True

# Game loop
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullets.append(ship.shoot())

    ship.update(keys)
    ship.draw(screen)

    for bullet in bullets[:]:
        bullet.update()
        bullet.draw(screen)
        if bullet.off_screen():
            bullets.remove(bullet)

    for asteroid in asteroids:
        asteroid.update()
        asteroid.draw(screen)

    # Colisiones bala - asteroide
    for bullet in bullets[:]:
        for asteroid in asteroids[:]:
            if (bullet.pos - asteroid.pos).length() < asteroid.radius:
                bullets.remove(bullet)
                asteroids.remove(asteroid)
                break

    pygame.display.flip()

pygame.quit()
