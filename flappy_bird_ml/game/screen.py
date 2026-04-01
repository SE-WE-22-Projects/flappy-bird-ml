import pygame

from flappy_bird_ml.game import colors, state
from flappy_bird_ml.game.constants import BIRD_X, PIPE_GAP, PIPE_WIDTH

GROUND_H = 60


class GameScreen:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def draw_background(self):
        pass

    def draw_bird(self, bird: state.Bird):
        pass

    def draw_pipe(self, pipe: state.Pipe):
        pass

    def show_frame(self):
        pass


class GameScreenPyGame(GameScreen):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)

        pygame.display.set_caption("Flappy Bird")

        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.offset = 0
        self.rect = self.screen.get_rect()

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

        bottom_y = pipe.gap_y + PIPE_GAP
        top_y = pipe.gap_y
        x = pipe.x - PIPE_WIDTH // 2

        # self.draw_rect(colors.GREEN, (x, pipe.gap_y, PIPE_WIDTH, PIPE_GAP))

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

    def show_frame(self):
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

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


pygame.init()
