import pygame
import sys
import random
import math

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Player
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 5
direction = "right"  # start retning

# Enemy
enemy_size = 50
enemy_x = random.randint(0, WIDTH)
enemy_y = random.randint(0, HEIGHT)
enemy_speed = 2

# Bullets
bullets = []
bullet_speed = 10

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Shoot
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append([player_x, player_y, direction])

    keys = pygame.key.get_pressed()

    # Movement + retning
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= player_speed
        direction = "left"
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += player_speed
        direction = "right"
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_y -= player_speed
        direction = "up"
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_y += player_speed
        direction = "down"

    # Hold på skjerm
    player_x = max(0, min(WIDTH - player_size, player_x))
    player_y = max(0, min(HEIGHT - player_size, player_y))

    # -------- Enemy følger spilleren --------
    dx = player_x - enemy_x
    dy = player_y - enemy_y
    distance = math.sqrt(dx**2 + dy**2)

    if distance != 0:
        enemy_x += (dx / distance) * enemy_speed
        enemy_y += (dy / distance) * enemy_speed

    # -------- Bullets --------
    for bullet in bullets[:]:
        if bullet[2] == "right":
            bullet[0] += bullet_speed
        elif bullet[2] == "left":
            bullet[0] -= bullet_speed
        elif bullet[2] == "up":
            bullet[1] -= bullet_speed
        elif bullet[2] == "down":
            bullet[1] += bullet_speed

        # fjern hvis utenfor skjerm
        if bullet[0] < 0 or bullet[0] > WIDTH or bullet[1] < 0 or bullet[1] > HEIGHT:
            bullets.remove(bullet)

    # Kollisjon (bullet vs enemy)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)

    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], 10, 5)
        if bullet_rect.colliderect(enemy_rect):
            bullets.remove(bullet)
            enemy_x = random.randint(0, WIDTH)
            enemy_y = random.randint(0, HEIGHT)

    # Draw
    screen.fill((30, 30, 30))

    # Player
    pygame.draw.rect(screen, (0, 200, 255),
                     (player_x, player_y, player_size, player_size))

    # Enemy
    pygame.draw.rect(screen, (255, 80, 80),
                     (enemy_x, enemy_y, enemy_size, enemy_size))

    # Bullets
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 255, 0),
                         (bullet[0], bullet[1], 10, 5))

    pygame.display.flip()
    clock.tick(60)