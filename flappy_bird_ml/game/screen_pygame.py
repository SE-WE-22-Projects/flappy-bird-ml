import random
import sys
from typing import Iterable

import pygame

from flappy_bird_ml.game import colors, state
from flappy_bird_ml.game.constants import BIRD_X, PIPE_GAP, PIPE_SPEED, PIPE_WIDTH
from flappy_bird_ml.game.screen import GameScreen
from flappy_bird_ml.game.util import text_shadow

pygame.init()

FONT_BIG = pygame.font.SysFont("Arial", 32, bold=True)
FONT_SMALL = pygame.font.SysFont("Arial", 22)
GROUND_H = 60


class GameScreenPyGame(GameScreen):
    """
    Screen that displays the game state using pygame.
    """

    def __init__(
        self,
        height: int,
        width: int,
        alg_name: str | None = None,
    ):
        pygame.display.set_caption("Flappy Bird")
        self.height = height
        self.width = width
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.offset = 0
        self.rect = self.screen.get_rect()
        self.clouds: list[Cloud] = [Cloud(width, i < 6) for i in range(20)]
        self.is_auto = alg_name is not None
        self.alg_name = alg_name
        self.speed_mult = 10

    def display(
        self,
        state: state.State,
        score: int,
        bird: state.Bird,
        pipes: Iterable[state.Pipe],
    ):
        self.offset += PIPE_SPEED
        self.draw_background()

        for c in self.clouds:
            c.draw(self.screen)
            c.update()
        self.clouds = [c for c in self.clouds if c.visible()]
        if len(self.clouds) < 6 and random.random() < 0.005:
            self.clouds.append(Cloud(self.width))

        self.draw_bird(bird)

        for pipe in pipes:
            self.draw_pipe(pipe)

        self.draw_ground()

        if state == "Playing":
            self.draw_score(score)
        elif state == "Ended":
            self._draw_game_over(score)
            self.offset = 0
        elif state == "Waiting":
            self._draw_start_screen()

        if self.is_auto:
            self.draw_auto_name()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                    self.speed_mult = min(100, self.speed_mult + 10)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                    self.speed_mult = max(10, self.speed_mult - 10)

            if self.speed_mult != 10:
                self.draw_speed()

        pygame.display.flip()
        self.clock.tick(6 * self.speed_mult)

    def draw_background(self):
        """
        Draw sky, clouds and ground
        """

        # sky color gradient
        for i in range(self.rect.h):
            t = i / max(self.rect.h - 1, 1)
            r = int(colors.SKY_TOP[0] + (colors.SKY_BOT[0] - colors.SKY_TOP[0]) * t)
            g = int(colors.SKY_TOP[1] + (colors.SKY_BOT[1] - colors.SKY_TOP[1]) * t)
            b = int(colors.SKY_TOP[2] + (colors.SKY_BOT[2] - colors.SKY_TOP[2]) * t)
            pygame.draw.line(
                self.screen,
                (r, g, b),
                (self.rect.x, self.rect.y + i),
                (self.rect.x + self.rect.w, self.rect.y + i),
            )

    def draw_ground(self):
        # ground dirt color
        gnd_y = self.rect.height - GROUND_H
        self.draw_rect(colors.DIRT_COL, (0, gnd_y + 18, self.rect.width, GROUND_H))
        self.draw_rect(colors.DIRT_COL, (0, gnd_y + 18, self.rect.width, GROUND_H))
        self.draw_rect(colors.GROUND_TOP, (0, gnd_y, self.rect.width, 22))
        self.draw_rect(colors.GROUND_BOT, (0, gnd_y + 22, self.rect.width, 8))

        # Scrolling grass tufts
        for i in range(-1, self.rect.width // 40 + 2):
            tx = i * 40 - self.offset % 40
            pygame.draw.ellipse(self.screen, colors.GROUND_TOP, (tx, gnd_y - 4, 22, 10))

    def draw_bird(self, bird: state.Bird):
        """
        Draw a bird
        """
        bird_surf = pygame.Surface((38, 28), pygame.SRCALPHA)

        # Body
        pygame.draw.ellipse(bird_surf, colors.YELLOW, (2, 6, 30, 20))
        pygame.draw.ellipse(bird_surf, colors.ORANGE, (2, 6, 30, 20), 2)

        # Wing
        wing_rect = pygame.Rect(8, 12, 16, 9)
        pygame.draw.ellipse(bird_surf, colors.ORANGE, wing_rect)
        pygame.draw.ellipse(bird_surf, (200, 120, 0), wing_rect, 1)

        # Eye
        pygame.draw.circle(bird_surf, colors.WHITE, (26, 10), 5)
        pygame.draw.circle(bird_surf, colors.BLACK, (27, 10), 3)
        pygame.draw.circle(bird_surf, colors.WHITE, (28, 9), 1)  # glint

        # Beak
        beak = [(32, 12), (38, 14), (32, 16)]
        pygame.draw.polygon(bird_surf, colors.ORANGE, beak)
        pygame.draw.polygon(bird_surf, (180, 80, 0), beak, 1)

        bird_angle = max(-30, min(90, bird.velocity * 5))
        rotated = pygame.transform.rotate(bird_surf, -bird_angle)
        rect = rotated.get_rect(center=(BIRD_X, bird.y))
        self.screen.blit(rotated, rect.topleft)

    def draw_pipe(self, pipe: state.Pipe):
        """Draw pipe."""
        cap_h = 24
        cap_w = PIPE_WIDTH + 8

        bottom_y = pipe.gap_bottom_y + PIPE_GAP
        top_y = pipe.gap_bottom_y
        x = pipe.x

        # self.draw_rect(
        #     colors.GREEN, (pipe.x - PIPE_WIDTH, pipe.gap_y, PIPE_WIDTH * 2, PIPE_GAP)
        # )

        for body_y, body_h, cap_y in [
            (0, top_y - cap_h, top_y - cap_h),  # top pipe
            (
                bottom_y + cap_h,
                self.rect.h - bottom_y - cap_h,
                bottom_y,
            ),  # bottom pipe
        ]:
            if body_h > 0:
                # Pipe body
                self.draw_rect(colors.PIPE_COL, (x + 2, body_y, PIPE_WIDTH - 2, body_h))

                # Highlight & shadow strips
                self.draw_rect(colors.PIPE_LIGHT, (x + 4, body_y, 8, body_h))
                self.draw_rect(
                    colors.PIPE_DARK, (x + PIPE_WIDTH - 8, body_y, 6, body_h)
                )

            # Cap
            self.draw_rect(
                colors.PIPE_COL, (x - 3, cap_y, cap_w, cap_h), border_radius=4
            )
            self.draw_rect(colors.PIPE_LIGHT, (x - 1, cap_y + 3, 10, cap_h - 6))
            self.draw_rect(
                colors.PIPE_DARK,
                (x + cap_w - 14, cap_y, 8, cap_h),
                border_radius=2,
            )

            self.draw_rect(
                colors.PIPE_DARK, (x - 3, cap_y, cap_w, cap_h), 2, border_radius=4
            )

    def draw_score(self, score: int):
        score_str = f"Score: {score}"
        sw = FONT_BIG.size(score_str)[0]
        text_shadow(
            self.screen, score_str, FONT_BIG, colors.WHITE, (self.width - sw) - 20, 20
        )

    def draw_speed(self):
        speed_str = f"Speed: {self.speed_mult // 10}X"
        sw, sh = FONT_SMALL.size(speed_str)
        text_shadow(
            self.screen,
            speed_str,
            FONT_SMALL,
            colors.WHITE,
            (self.width - sw) - 20,
            (self.height - sh) - 20,
        )

    def _draw_start_screen(self):
        title_w = FONT_BIG.size("Flappy Bird")[0]
        text_shadow(
            self.screen,
            "Flappy Bird",
            FONT_BIG,
            colors.YELLOW,
            (self.width - title_w) // 2,
            220,
        )

        hint = "Press SPACE to flap"
        hw = FONT_SMALL.size(hint)[0]
        text_shadow(
            self.screen, hint, FONT_SMALL, colors.WHITE, (self.width - hw) // 2, 292
        )

    def _draw_game_over(self, score: int):
        go_w = FONT_BIG.size("Game Over")[0]
        text_shadow(
            self.screen,
            "Game Over",
            FONT_BIG,
            colors.RED,
            (self.width - go_w) // 2,
            190,
        )

        sc_txt = f"Score : {score}"
        sc_w = FONT_SMALL.size(sc_txt)[0]
        text_shadow(
            self.screen, sc_txt, FONT_SMALL, colors.WHITE, (self.width - sc_w) // 2, 258
        )

        restart = "SPACE to restart"
        rw = FONT_SMALL.size(restart)[0]
        text_shadow(
            self.screen, restart, FONT_SMALL, colors.WHITE, (self.width - rw) // 2, 350
        )

    def draw_auto_name(self):
        alg_str = f"Algorithm: {self.alg_name}"
        text_shadow(self.screen, alg_str, FONT_SMALL, colors.WHITE, 10, 10)

    def should_retry(self) -> bool:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.K_SPACE:
                    return True

    def wait_input(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return

    def draw_rect(
        self,
        color: tuple[int, int, int],
        rect: tuple[int, int, int, int],
        width: int = 0,
        border_radius: int = -1,
    ):
        pygame.draw.rect(
            self.screen, color, rect, width=width, border_radius=border_radius
        )


class Cloud:
    def __init__(self, screen_width: int, initial: bool = False):
        self.x = random.randint(0, 200) + (0 if initial else screen_width)
        self.y = random.randint(40, 220)
        self.scale = random.uniform(0.6, 1.2)
        self.speed = random.uniform(0.4, 0.9)

    def update(self):
        self.x -= self.speed

    def visible(self):
        return self.x + 20 * 2 * self.scale > 0

    def draw(self, surface):
        s = self.scale
        cx = int(self.x)
        cy = int(self.y)
        for dx, dy, r in [
            (0, 0, 22),
            (-18, 8, 16),
            (18, 8, 16),
            (-8, 14, 12),
            (8, 14, 12),
        ]:
            pygame.draw.circle(
                surface, colors.WHITE, (cx + int(dx * s), cy + int(dy * s)), int(r * s)
            )
