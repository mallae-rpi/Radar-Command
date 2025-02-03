import pygame
import math
from gamestate import GameState
from missile import Missile
from crosshair import Crosshair
from typing import Tuple, List

def init_game() -> Tuple[pygame.Surface, pygame.font.Font]:
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Radar Command")
    return screen, pygame.font.Font(None, 36)

def handle_events() -> bool:
    event: pygame.Eventlist
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def handle_controls(crosshair: Crosshair) -> None:
    keys: pygame.bools = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        crosshair.move(-1, 0, WIDTH, HEIGHT)
    if keys[pygame.K_d]:
        crosshair.move(1, 0, WIDTH, HEIGHT)
    if keys[pygame.K_w]:
        crosshair.move(0, -1, WIDTH, HEIGHT)
    if keys[pygame.K_s]:
        crosshair.move(0, 1, WIDTH, HEIGHT)

def check_missile_destruction(missiles: List[Missile], crosshair: Crosshair, game_state: GameState) -> None:
    keys: pygame.bools = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        for missile in missiles:
            if missile.active and math.hypot(missile.x - crosshair.x, missile.y - crosshair.y) < EXPLOSION_RADIUS:
                missile.active = False
                game_state.hit_missiles += 1

def update_missiles(missiles: List[Missile], screen: pygame.Surface, game_state: GameState) -> None:
    for missile in missiles:
        if missile.active:
            missile.move()
            missile.draw(screen, WHITE)
            pygame.draw.circle(screen, WHITE, RADAR_CENTER, 5, 1)  # Hollow circle for missile impact indicator
            if not missile.active and math.hypot(missile.x - RADAR_CENTER[0], missile.y - RADAR_CENTER[1]) < 5:
                game_state.missed_missiles += 1
    missiles[:] = [m for m in missiles if m.active]  # Remove inactive missiles
    while len(missiles) < 5:  # Ensure missiles keep spawning
        missiles.append(Missile(RADAR_CENTER, WIDTH, HEIGHT, MISSILE_SPEED))

def draw_game(screen: pygame.Surface, font: pygame.font.Font, crosshair: Crosshair, missiles: List[Missile], game_state: GameState) -> None:
    screen.fill(BLACK)
    pygame.draw.circle(screen, WHITE, RADAR_CENTER, WIDTH // 2, 1)
    update_missiles(missiles, screen, game_state)
    crosshair.draw(screen, WHITE)
    hit_missiles_text: pygame.Surface = font.render(f"Hit: {game_state.hit_missiles}", True, WHITE)
    screen.blit(hit_missiles_text, (10, 10))
    missed_text: pygame.Surface = font.render(f"Missed: {game_state.missed_missiles}", True, WHITE)
    screen.blit(missed_text, (10, 40))
    pygame.display.flip()

def main() -> None:
    screen, font = init_game()
    missiles: List[Missile] = [Missile(RADAR_CENTER, WIDTH, HEIGHT, MISSILE_SPEED) for _ in range(5)]
    crosshair: Crosshair = Crosshair(WIDTH, HEIGHT, CROSSHAIR_SPEED)
    game_state = GameState()
    running: bool = True
    
    while running:
        running = handle_events()
        handle_controls(crosshair)
        check_missile_destruction(missiles, crosshair, game_state)
        draw_game(screen, font, crosshair, missiles, game_state)
        pygame.time.delay(30)
    
    pygame.quit()

if __name__ == "__main__":
    WIDTH: int = 800
    HEIGHT: int = 600
    RADAR_CENTER: Tuple[int, int] = (WIDTH // 2, HEIGHT // 2)
    MISSILE_SPEED: int = 2
    CROSSHAIR_SPEED: int = 4
    EXPLOSION_RADIUS: int = 30
    
    BLACK: Tuple[int, int, int] = (0, 0, 0)
    WHITE: Tuple[int, int, int] = (255, 255, 255)
    
    main()