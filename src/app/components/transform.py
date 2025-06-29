import pygame


class Transform:
    def __init__(self, x: float, y: float, width: int = 0, height: int = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(int(x), int(y), width, height)

    def update_rect(self):
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.rect.width = self.width
        self.rect.height = self.height

    def set_position(self, x: float, y: float):
        self.x = x
        self.y = y
        self.update_rect()

    # tem que receber já multiplicado pelo delta time
    def move(self, dx: float, dy: float):
        self.x += dx
        self.y += dy
        self.update_rect()
