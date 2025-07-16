from app.components.transform import Transform


class Movement:
    def __init__(
        self,
        speed: float = 1000.0,
        gravity: float = 2000.0,
        jump_velocity: float = -800.0,
    ):
        self.speed = speed
        self.gravity = gravity
        self.jump_velocity = jump_velocity

        self.vx = 0.0
        self.vy = 0.0
        self.is_on_ground = False

    def set_horizontal_velocity(self, direction: float):
        # -1 Esquerda
        # 0 Parado
        # 1 Direita
        if direction not in (-1.0, 0.0, 1.0):
            raise ValueError("Direction must be -1, 0, or 1")

        self.vx = direction * self.speed

    def jump(self):
        if self.is_on_ground:
            self.vy = self.jump_velocity
            self.is_on_ground = False
            return True
        return False

    def apply_gravity(self, delta_time: float):
        if not self.is_on_ground:
            self.vy += self.gravity * delta_time

    def update_position(self, transform: Transform, delta_time: float):
        dx = self.vx * delta_time
        dy = self.vy * delta_time
        transform.move(dx, dy)
