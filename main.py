import pygame
import random

# Starter pygame
pygame.init()

# Vindu
WIDTH = 900
HEIGHT = 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dinosaur Game")

# FPS
clock = pygame.time.Clock()
FPS = 60

# Farger
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (100, 200, 100)

# Bilder
player_img = pygame.image.load("dino.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (60, 60))

coin_img = pygame.image.load("coin.png").convert_alpha()
coin_img = pygame.transform.scale(coin_img, (35, 35))

spike_img = pygame.image.load("spikes.png").convert_alpha()
spike_img = pygame.transform.scale(spike_img, (55, 55))

# Spiller
player = pygame.Rect(100, 290, 60, 60)

# Enemy
enemy = pygame.Rect(900, 295, 55, 55)
enemy_speed = 7

# Coin
coin = pygame.Rect(600, 220, 35, 35)
coin_speed = 5

# Fysikk
velocity = 0
gravity = 1
jump_power = -17

# Score
score = 0

# Font
font = pygame.font.SysFont("Arial", 36)

# Funksjon for å flytte coin
def move_coin():
    coin.x = WIDTH + random.randint(200, 500)
    coin.y = random.randint(180, 300)

# Spill-løkke
run = True

while run:

    clock.tick(FPS)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Tastatur
    keys = pygame.key.get_pressed()

    # Hopp
    if keys[pygame.K_SPACE] and player.y >= 290:
        velocity = jump_power

    # Gravity
    velocity += gravity
    player.y += velocity

    # Bakke-kollisjon
    if player.y > 290:
        player.y = 290
        velocity = 0

    # Flytt enemy
    enemy.x -= enemy_speed

    # Reset enemy
    if enemy.x < -60:
        enemy.x = WIDTH + random.randint(100, 300)

    # Flytt coin
    coin.x -= coin_speed

    # Reset coin hvis den går ut av skjermen
    if coin.x < -40:
        move_coin()

    # Coin collision
    if player.colliderect(coin):
        score += 1
        move_coin()

    # Enemy collision
    if player.colliderect(enemy):
        print("GAME OVER")
        print("Final Score:", score)
        run = False

    # Tegn bakgrunn
    screen.fill(WHITE)

    # Gress
    pygame.draw.rect(screen, GREEN, (0, 350, WIDTH, 100))

    # Bakke-linje
    pygame.draw.line(screen, BLACK, (0, 350), (WIDTH, 350), 3)

    # Tegn objekter
    screen.blit(player_img, (player.x, player.y))
    screen.blit(spike_img, (enemy.x, enemy.y))
    screen.blit(coin_img, (coin.x, coin.y))

    # Score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (20, 20))

    # Oppdater skjerm
    pygame.display.update()

# Avslutt pygame
pygame.quit()
#Test