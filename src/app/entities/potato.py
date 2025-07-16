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
from pygame.sprite import spritecollide
import pygame
from app.entities.idle_character import IdleCharacter


class Potato(Observable):
    def __init__(self, x: float, y: float):
        self.logger = logging.getLogger(__name__)
        Observable.__init__(self)

        # Inicializa componentes
        self.animation_component = AnimationComponent("potato")
        first_frame = self.animation_component.get_current_frame()
        width = first_frame.get_width()
        height = first_frame.get_height()

        self.transform = Transform(x, y, width, height)
        self.movement = Movement(speed=500.0, gravity=2000.0, jump_velocity=-800.0)
        self.input_handler = InputHandler()
        self.renderer = Render(self.animation_component)
        self.collision_handler = CollisionHandler()

        self.rect = pygame.Rect(
            self.transform.x,
            self.transform.y,
            self.transform.width,
            self.transform.height,
        )
        self.facing_right = True

        # Modo de depuração
        self.is_debug_mode = False
        self.f1_key_pressed = False

        # Pulo
        self.is_charging_jump = False
        self.charge_time = 0.0
        self.max_charge_time = 1.0
        self.was_space_pressed = False

        # Controle de movimento aéreo
        self.air_direction_locked = False
        self.air_movement_disabled_by_wall = False

    def handle_input_and_movement(self, delta_time: float) -> None:
        left, right, jump = self.input_handler.get_movement_input()

        if self.movement.is_on_ground:
            self.movement.vx = 0.0

        moved = False
        if not self.air_movement_disabled_by_wall:
            if self.movement.is_on_ground or not self.air_direction_locked:
                if left:
                    self.movement.set_horizontal_velocity(-1.0)
                    self.facing_right = False
                    moved = True
                elif right:
                    self.movement.set_horizontal_velocity(1.0)
                    self.facing_right = True
                    moved = True

                # trava a direção no ar se o personagem já se moveu pulando
                if not self.movement.is_on_ground and moved:
                    self.air_direction_locked = True

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
            self._execute_charged_jump()
            self.is_charging_jump = False
            self.charge_time = 0.0

        self.was_space_pressed = jump

        self.movement.apply_gravity(delta_time)

        # atualização de animações
        if moved:
            self.animation_component.change_state(AnimationState.RUN)
        elif not self.movement.is_on_ground:
            self.animation_component.change_state(AnimationState.JUMP)
        else:
            self.animation_component.change_state(AnimationState.IDLE)

        self.animation_component.set_facing_direction(self.facing_right)

    def handle_debug_movement(self, delta_time: float) -> None:
        left, right, up, down = self.input_handler.get_debug_movement_input()

        self.movement.vx = 0
        self.movement.vy = 0

        if left:
            self.movement.set_horizontal_velocity(-1.0)
            self.facing_right = False
        elif right:
            self.movement.set_horizontal_velocity(1.0)
            self.facing_right = True

        if up:
            self.movement.vy = -self.movement.speed
        elif down:
            self.movement.vy = self.movement.speed

        self.transform.x += self.movement.vx * delta_time
        self.transform.y += self.movement.vy * delta_time

    def _execute_charged_jump(self):
        self.logger.info(f"x:{self.transform.x} y:{self.transform.y}")
        charge = self.charge_time / self.max_charge_time
        min_multiplier = 0.3
        max_multiplier = 2.0
        jump_multiplier = min_multiplier + (max_multiplier - min_multiplier) * charge

        base_jump_velocity = self.movement.jump_velocity
        self.movement.vy = base_jump_velocity * jump_multiplier
        self.movement.is_on_ground = False

        self.logger.info(
            f"Jumped with {charge * 100:.1f}% charge (multiplier: {jump_multiplier:.2f})"
        )

    def check_friend_collision(self, idle_characters: pygame.sprite.Group):
        collided_friends = spritecollide(self, idle_characters, True)
        for friend in collided_friends:
            if isinstance(friend, IdleCharacter):
                self.notify_observers(
                    f"rescued_{friend.animation_component.character_name}"
                )

    def update(
        self,
        delta_time: float,
        tiles: List[Tile],
        window_width: int,
        window_height: int,
        idle_characters: pygame.sprite.Group,
    ) -> None:
        f1_pressed = self.input_handler.get_toggle_debug_input()
        if f1_pressed and not self.f1_key_pressed:
            self.is_debug_mode = not self.is_debug_mode
            self.logger.info(
                f"Modo de depuração {'ativado' if self.is_debug_mode else 'desativado'}"
            )
            self.movement.vx = 0
            self.movement.vy = 0
        self.f1_key_pressed = f1_pressed

        if self.is_debug_mode:
            self.handle_debug_movement(delta_time)
        else:
            was_on_ground = self.movement.is_on_ground

            self.handle_input_and_movement(delta_time)

            # faz o quique com a mesma velocidade horizontal antes de colidir com a parede
            vx_before_collision = self.movement.vx

            self.collision_handler.handle_collisions(
                self.transform, self.movement, tiles, delta_time
            )

            if (
                not self.movement.is_on_ground
                and vx_before_collision != 0
                and self.movement.vx == 0
            ):
                self.movement.vx = -vx_before_collision  # inverte
                self.air_movement_disabled_by_wall = True  # trava o controle
                self.facing_right = (
                    not self.facing_right
                )  # espelha o personagem pra mostrar que ta indo pro outro lado

            self.movement.is_on_ground = self.collision_handler.check_on_ground(
                self.transform, tiles
            )

            # reseta os controles travados de quando estava no ar se o personagem pousou
            if not was_on_ground and self.movement.is_on_ground:
                self.air_direction_locked = False
                self.air_movement_disabled_by_wall = False

        self.rect.topleft = (self.transform.x, self.transform.y)

        self.check_friend_collision(idle_characters)

        boundary_hit = self.collision_handler.check_bounds(
            self.transform, self.movement, window_width, window_height
        )

        if boundary_hit:
            self.notify_observers(boundary_hit)

        self.renderer.update(delta_time)

    def draw(self, window: Window) -> None:
        self.renderer.draw(window, self.transform)
