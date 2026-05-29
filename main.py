import random
import sys
from dataclasses import dataclass
from typing import List

import pygame

WIDTH, HEIGHT = 800, 600
FPS = 60

BG = (30, 30, 30)
PLAYER_COLOR = (0, 200, 255)
ENEMY_COLOR = (255, 80, 80)
BULLET_COLOR = (255, 255, 0)
CROSSHAIR_COLOR = (255, 255, 255)

PLAYER_SIZE = 50
ENEMY_SIZE = 50
PLAYER_SPEED = 5
ENEMY_SPEED = 2
BULLET_SPEED = 10
BULLET_SIZE = (10, 5)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Shooter")
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()


@dataclass
class Entity:
    rect: pygame.Rect
    color: tuple
    speed: float


@dataclass
class Bullet:
    rect: pygame.Rect
    velocity: pygame.math.Vector2


def clamp_rect(rect: pygame.Rect) -> None:
    rect.left = max(0, min(WIDTH - rect.width, rect.left))
    rect.top = max(0, min(HEIGHT - rect.height, rect.top))


def create_enemy() -> Entity:
    x = random.randint(0, WIDTH - ENEMY_SIZE)
    y = random.randint(0, HEIGHT - ENEMY_SIZE)
    return Entity(pygame.Rect(x, y, ENEMY_SIZE, ENEMY_SIZE), ENEMY_COLOR, ENEMY_SPEED)


def create_bullet(center: tuple[int, int], direction: pygame.math.Vector2) -> Bullet:
    rect = pygame.Rect(0, 0, *BULLET_SIZE)
    rect.center = center
    velocity = direction.normalize() * BULLET_SPEED
    return Bullet(rect, velocity)


def main() -> None:
    player = Entity(
        pygame.Rect(WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT // 2 - PLAYER_SIZE // 2, PLAYER_SIZE, PLAYER_SIZE),
        PLAYER_COLOR,
        PLAYER_SPEED,
    )
    enemy = create_enemy()
    bullets: List[Bullet] = []
    player_direction = pygame.math.Vector2(1, 0)

    while True:
        keys = pygame.key.get_pressed()
        move = pygame.math.Vector2(0, 0)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move.x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move.y += 1

        if move.length_squared() > 0:
            player_direction = move.normalize()
            player.rect.move_ip(player_direction * player.speed)

        clamp_rect(player.rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullets.append(create_bullet(player.rect.center, player_direction))

        enemy_vector = pygame.math.Vector2(player.rect.center) - pygame.math.Vector2(enemy.rect.center)
        if enemy_vector.length_squared() > 0:
            enemy.rect.move_ip(enemy_vector.normalize() * enemy.speed)
            clamp_rect(enemy.rect)

        next_bullets: List[Bullet] = []
        for bullet in bullets:
            bullet.rect.move_ip(bullet.velocity)
            if not screen.get_rect().colliderect(bullet.rect):
                continue
            if bullet.rect.colliderect(enemy.rect):
                enemy = create_enemy()
                continue
            next_bullets.append(bullet)

        bullets = next_bullets

        screen.fill(BG)
        pygame.draw.rect(screen, player.color, player.rect)
        pygame.draw.rect(screen, enemy.color, enemy.rect)

        for bullet in bullets:
            pygame.draw.rect(screen, BULLET_COLOR, bullet.rect)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.circle(screen, CROSSHAIR_COLOR, (mouse_x, mouse_y), 15, 2)
        pygame.draw.line(screen, CROSSHAIR_COLOR, (mouse_x - 20, mouse_y), (mouse_x + 20, mouse_y), 2)
        pygame.draw.line(screen, CROSSHAIR_COLOR, (mouse_x, mouse_y - 20), (mouse_x, mouse_y + 20), 2)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()