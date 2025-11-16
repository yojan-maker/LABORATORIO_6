  GNU nano 7.2                                                                                                                                                                                         main.py *                                                                                                                                                                                                
import pygame
import threading
import time
from game_objects import Player, Enemy, Platform, Coin 
from config import WIDTH, HEIGHT, BLACK

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer con Hilos")
clock = pygame.time.Clock()

# Fuente para Game Over
font = pygame.font.SysFont("Arial", 48)
font_small = pygame.font.SysFont("Arial", 24)

# Fondo
background = pygame.image.load("assets/background.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Crear jugador
player = Player(100, 500)

# Función para crear enemigos
def create_enemies():
    enemies = []
    positions = [
        (230, 480),
        (480, 400),
        (170, 300),
        (450, 220),
        (280, 130)
    ]
    for pos in positions:
        enemies.append(Enemy(*pos))
    return enemies

enemies = create_enemies()

# Plataformas 
platforms = [
    Platform(0, 560, 800, 40),
    Platform(200, 460, 180, 20),
    Platform(450, 380, 180, 20),
    Platform(150, 280, 160, 20),
    Platform(420, 200, 200, 20),
    Platform(250, 90, 150, 20)
]

# --------------------------
# COINS 
# --------------------------
coins = [
    Coin(260, 430),
    Coin(500, 350),
    Coin(200, 260),
    Coin(480, 180),
    Coin(290, 60),
]

TOTAL_COINS = len(coins)
score = 0

# Sistema de hilos
mutex = threading.Lock()
running = True

def enemy_thread():
    while running:
        with mutex:
            for e in enemies:
                e.update(platforms)
        time.sleep(0.016)

threading.Thread(target=enemy_thread, daemon=True).start()

# Game Over
def game_over_screen():
    screen.fill((0, 0, 0))
    text = font.render("GAME OVER", True, (255, 0, 0))
    msg = font_small.render("Presiona cualquier tecla para salir", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 200))
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 300))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                exit()

# Pantalla de victoria
def win_screen():
    screen.fill((0, 0, 0))
    text = font.render("¡GANASTE!", True, (255, 255, 0))
    msg = font_small.render("Recolectaste todas las monedas", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 200))
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 300))
    pygame.display.flip()

    time.sleep(3)
    pygame.quit()
    exit()

# Función respawn
def respawn():
    global enemies
    player.rect.x = 100
    player.rect.y = 500
    player.vel.x = 0
    player.vel.y = 0
    player.on_ground = False
    enemies = create_enemies()

# Loop principal
running_game = True
while running_game:

    if player.lives <= 0:
        game_over_screen()

    if score == TOTAL_COINS:
        win_screen()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_game = False

    screen.blit(background, (0, 0))

    keys = pygame.key.get_pressed()
    player.handle_input(keys)
    player.update(platforms)

    # Colisión con enemigos
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            player.lives -= 1
            respawn()
            break

    # Caída del mapa
    if player.rect.y > HEIGHT + 200:
        player.lives -= 1
        respawn()

    # Colisión con coins
    for c in coins[:]:
        if player.rect.colliderect(c.rect):
            coins.remove(c)
            score += 1

    # Dibujar
    for p in platforms:
        p.draw(screen)

    for c in coins:
        c.draw(screen)

    for enemy in enemies:
        enemy.draw(screen)

    player.draw(screen)

    # Score
    score_text = font_small.render(f"Score: {score}/{TOTAL_COINS}", True, (255, 255, 0))
    screen.blit(score_text, (WIDTH - 200, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
