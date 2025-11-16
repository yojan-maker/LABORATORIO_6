import pygame

class Player:
    def __init__(self, x, y, w=40, h=60):
        self.rect = pygame.Rect(x, y, w, h)
        self.vel = pygame.Vector2(0, 0)
        self.speed = 5
        self.jump_force = -16
        self.gravity = 0.8
        self.on_ground = False
        self.lives = 3

        self.image = pygame.image.load("assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (w, h))

        self.font = pygame.font.SysFont("Arial", 24)

    def handle_input(self, keys):
        self.vel.x = 0
        if keys[pygame.K_LEFT]:
            self.vel.x = -self.speed
        if keys[pygame.K_RIGHT]:
            self.vel.x = self.speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel.y = self.jump_force
            self.on_ground = False

    def apply_gravity(self):
        self.vel.y += self.gravity
        if self.vel.y > 20:
            self.vel.y = 20

    def update(self, platforms):
        self.apply_gravity()

        # Movimiento X
        self.rect.x += self.vel.x
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel.x > 0:
                    self.rect.right = p.rect.left
                elif self.vel.x < 0:
                    self.rect.left = p.rect.right

        # Movimiento Y
        self.rect.y += self.vel.y
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel.y > 0:
                    self.rect.bottom = p.rect.top
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:

 def draw(self, screen):
        screen.blit(self.image, self.rect)
        lives_text = self.font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 10))


class Enemy:
    def __init__(self, x, y, w=40, h=60):
        self.rect = pygame.Rect(x, y, w, h)
        self.vel = pygame.Vector2(2, 0)
        self.gravity = 0.8

        self.image = pygame.image.load("assets/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (w, h))

    def apply_gravity(self):
        self.vel.y += self.gravity
        if self.vel.y > 20:
            self.vel.y = 20

    def on_platform(self, platforms):
        self.rect.y += 2
        on_top = any(self.rect.colliderect(p.rect) for p in platforms)
        self.rect.y -= 2
        return on_top

    def update(self, platforms):
        self.apply_gravity()

        # Movimiento horizontal
        self.rect.x += self.vel.x

        # Detectar borde
        if not self.on_platform(platforms):
            self.vel.x *= -1
            self.rect.x += self.vel.x * 2

        # Colisiones laterales
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel.x > 0:
                    self.rect.right = p.rect.left
                else:
                    self.rect.left = p.rect.right
                self.vel.x *= -1

        # Movimiento vertical
        self.rect.y += self.vel.y
        landed = False
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vel.y > 0:

 landed = True

        if not landed:
            self.vel.y += self.gravity

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Platform:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (150, 100, 80)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Coin:
    def __init__(self, x, y, size=24):
        # rect de la moneda (hitbox)
        self.rect = pygame.Rect(x, y, size, size)
        self.collected = False

        # cargar imagen si existe en assets/coin.png; si no, se usará un relleno amarillo
        try:
            self.image = pygame.image.load("assets/coin.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (size, size))
        except Exception:
            self.image = None

    def draw(self, screen):
        if self.collected:
            return
        if self.image:
            screen.blit(self.image, self.rect)
        else:
            pygame.draw.ellipse(screen, (255, 220, 0), self.rect)

    def collect(self):
        self.collected = True
