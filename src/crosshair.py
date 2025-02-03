import pygame
from typing import Tuple

class Crosshair:
    def __init__(self, width: int, height: int, speed: int) -> None:
        self.x: int = width // 2
        self.y: int = height // 2
        self.speed: int = speed

    def move(self, dx: int, dy: int, width: int, height: int) -> None:
        self.x = max(0, min(width, self.x + dx * self.speed))
        self.y = max(0, min(height, self.y + dy * self.speed))

    def draw(self, screen: pygame.Surface, color: Tuple[int, int, int]) -> None:
        pygame.draw.line(screen, color, (self.x - 10, self.y), (self.x + 10, self.y), 2)
        pygame.draw.line(screen, color, (self.x, self.y - 10), (self.x, self.y + 10), 2)