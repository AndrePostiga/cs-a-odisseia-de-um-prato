from app.core.observer import Observable
from app.entities.tile import Tile
from app.pplay.window import Window
from app.core.animation_state import AnimationState
from app.components.movement import Movement
from app.components.animation_component import AnimationComponent
from app.components.input_handler import InputHandler
from app.components.transform import Transform
from app.components.render import Render
from app.core.collision_system import CollisionHandler
from typing import List
import logging


class Potato(Observable):
    def __init__(self, x: float, y: float):
        self.logger = logging.getLogger(__name__)
        Observable.__init__(self)

        # Inicializa componentes
        self.animation_component = AnimationComponent()
        first_frame = self.animation_component.get_current_frame()
        width = first_frame.get_width()
        height = first_frame.get_height()

        self.transform = Transform(x, y, width, height)
        self.movement = Movement(speed=1000.0, gravity=2000.0, jump_velocity=-800.0)
        self.input_handler = InputHandler()
        self.renderer = Render(self.animation_component)
        self.collision_handler = CollisionHandler()

        self.facing_right = True

        # Pulo
        self.is_charging_jump = False
        self.charge_time = 0.0
        self.max_charge_time = 1.0
        self.was_space_pressed = False

    def handle_input_and_movement(self, delta_time: float) -> None:
        left, right, jump = self.input_handler.get_movement_input()

        # movimento horizontal
        self.movement.vx = 0.0
        moved = False

        if left:
            self.movement.set_horizontal_velocity(-1.0)
            self.facing_right = False
            moved = True
        elif right:
            self.movement.set_horizontal_velocity(1.0)
            self.facing_right = True
            moved = True

        # Pulo
        if jump and self.movement.is_on_ground:
            if not self.was_space_pressed:
                self.is_charging_jump = True
                self.charge_time = 0.0
            else:
                self.charge_time += delta_time
                if self.charge_time > self.max_charge_time:
                    self.charge_time = self.max_charge_time

        elif not jump and self.was_space_pressed and self.is_charging_jump:
            # Quando soltar espaço fazer o pulo
            self._execute_charged_jump()
            self.is_charging_jump = False
            self.charge_time = 0.0

        self.was_space_pressed = jump

        # Gravidade
        self.movement.apply_gravity(delta_time)

        # Atualizar Animações
        if moved:
            self.animation_component.change_state(AnimationState.RUN)
        elif not self.movement.is_on_ground:
            self.animation_component.change_state(AnimationState.JUMP)
        else:
            self.animation_component.change_state(AnimationState.IDLE)

        self.animation_component.set_facing_direction(self.facing_right)

    def _execute_charged_jump(self):
        """Execute jump based on charge time."""
        # Calculate jump multiplier (0.3 to 2.0 based on charge time)
        charge_ratio = self.charge_time / self.max_charge_time
        min_multiplier = 0.3
        max_multiplier = 2.0
        jump_multiplier = (
            min_multiplier + (max_multiplier - min_multiplier) * charge_ratio
        )

        # Apply jump with multiplier
        base_jump_velocity = self.movement.jump_velocity
        self.movement.vy = base_jump_velocity * jump_multiplier
        self.movement.is_on_ground = False

        print(
            f"Jumped with {charge_ratio * 100:.1f}% charge (multiplier: {jump_multiplier:.2f})"
        )

    def update(
        self,
        delta_time: float,
        tiles: List[Tile],
        window_width: int,
        window_height: int,
    ) -> None:
        self.handle_input_and_movement(delta_time)

        self.collision_handler.handle_collisions(
            self.transform, self.movement, tiles, delta_time
        )

        self.movement.is_on_ground = self.collision_handler.check_on_ground(
            self.transform, tiles
        )

        boundary_hit = self.collision_handler.check_bounds(
            self.transform, self.movement, window_width, window_height
        )
        if boundary_hit:
            self.notify_observers(boundary_hit)

        self.renderer.update(delta_time)

    def draw(self, window: Window) -> None:
        self.renderer.draw(window, self.transform)
