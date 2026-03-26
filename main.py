import pygame
import sys
import random

pygame.init()

# Skjerm
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake + Random Fruit")

clock = pygame.time.Clock()

# Spiller
player_size = 50
player_x = WIDTH // 2
player_y = HEIGHT // 2
speed = 5

# Frukt (random start)
fruit_size = 50
fruit_x = random.randint(0, WIDTH - fruit_size)
fruit_y = random.randint(0, HEIGHT - fruit_size)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Bevegelse
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_y -= speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_y += speed

    # Hold spilleren på skjermen
    player_x = max(0, min(WIDTH - player_size, player_x))
    player_y = max(0, min(HEIGHT - player_size, player_y))

    # Kollisjon (ny random frukt)
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    fruit_rect = pygame.Rect(fruit_x, fruit_y, fruit_size, fruit_size)

    if player_rect.colliderect(fruit_rect):
        fruit_x = random.randint(0, WIDTH - fruit_size)
        fruit_y = random.randint(0, HEIGHT - fruit_size)

    # Tegning
    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (0, 200, 255), player_rect)  # spiller (blå)
    pygame.draw.rect(screen, (255, 0, 0), fruit_rect)     # frukt (rød)

    pygame.display.flip()
    clock.tick(60)