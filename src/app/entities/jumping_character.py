import random
from app.pplay.sprite import Sprite
from app.components.movement import Movement
from app.components.transform import Transform


class JumpingCharacter:
    def __init__(self, image_path: str, x: float, y: float):
        self.transform = Transform(x, y)
        self.sprite = Sprite(image_path)
        self.movement = Movement(
            speed=0, gravity=800
        )  # Apenas movimento vertical por gravidade
        self.movement.vy = -random.randint(400, 700)  # Impulso inicial

    def update(self, delta_time: float):
        self.movement.apply_gravity(delta_time)
        self.transform.y += self.movement.vy * delta_time

    def draw(self):
        self.sprite.set_position(self.transform.x, self.transform.y)
        self.sprite.draw()
