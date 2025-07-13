from app.components.animation_component import AnimationComponent
import pygame


class IdleCharacter(pygame.sprite.Sprite):
    def __init__(self, x: float, y: float, character_name: str, flipped: bool = False):
        super().__init__()
        self.animation_component = AnimationComponent(character_name)

        self.image = self.animation_component.get_current_frame()
        self.rect = self.image.get_rect(topleft=(x, y))

        self.animation_component.set_facing_direction(not flipped)

    def update(self, delta_time: float):
        self.animation_component.update(delta_time)
        self.image = self.animation_component.get_current_frame()
