import pygame
import random

pygame.init()

# Window
WIDTH = 800
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Images
player_img = pygame.transform.scale(
    pygame.image.load("dino.png"), (60, 60)
)

coin_img = pygame.transform.scale(
    pygame.image.load("coin.png"), (35, 35)
)

spike_img = pygame.transform.scale(
    pygame.image.load("spikes.png"), (50, 50)
)

# Player
player = pygame.Rect(100, 290, 60, 60)

# Spike
enemy = pygame.Rect(700, 300, 50, 50)

# Coin
coin = pygame.Rect(500, 250, 35, 35)

# Jump
velocity = 0
gravity = 1

# Score
score = 0
font = pygame.font.SysFont(None, 40)

# Game loop
run = True
while run:

    clock.tick(60)

    # Close game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Jump
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and player.y == 290:
        velocity = -15

    # Gravity
    velocity += gravity
    player.y += velocity

    # Ground
    if player.y > 290:
        player.y = 290
        velocity = 0

    # Move spike
    enemy.x -= 6

    coin.x -= 4

    if enemy.x < -50:
        enemy.x = WIDTH

    # Smaller spike hitbox
    spike_box = pygame.Rect(enemy.x + 10, enemy.y + 15, 30, 25)

    # Hit spike
    if player.colliderect(spike_box):
        print("GAME OVER")
        run = False

    # Get coin
    if player.colliderect(coin):
        score += 1
        coin.x = random.randint(300, 750)
        coin.y = random.randint(180, 300)

    # Background
    screen.fill(WHITE)

    # Ground line
    pygame.draw.line(screen, BLACK, (0, 350), (WIDTH, 350), 3)

    # Draw images
    screen.blit(player_img, (player.x, player.y))
    screen.blit(spike_img, (enemy.x, enemy.y))
    screen.blit(coin_img, (coin.x, coin.y))

    # Score text
    text = font.render("Score: " + str(score), True, BLACK)
    screen.blit(text, (20, 20))

    pygame.display.update()

pygame.quit()