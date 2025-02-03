import math
import pygame
import random
from typing import Tuple

class Missile:
    def __init__(self, radar_center: Tuple[int, int], width: int, height: int, speed: int) -> None:
        self.x: float
        self.y: float
        self.x, self.y = radar_center
        angle: float = random.uniform(0, 2 * math.pi)
        self.x += math.cos(angle) * (width // 2)
        self.y += math.sin(angle) * (height // 2)
        self.target_x: int = radar_center[0]
        self.target_y: int = radar_center[1]
        self.angle: float = math.atan2(self.target_y - self.y, self.target_x - self.x)
        self.active: bool = True
        self.speed: int = speed

    def move(self) -> None:
        if self.active:
            self.x += self.speed * math.cos(self.angle)
            self.y += self.speed * math.sin(self.angle)
            if math.hypot(self.x - self.target_x, self.y - self.target_y) < 5:
                self.active = False  # Missile reached center

    def draw(self, screen: pygame.Surface, color: Tuple[int, int, int]) -> None:
        if self.active:
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), 5)
