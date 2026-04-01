import pygame

from flappy_bird_ml.game import colors

GROUND_H = 60


class GameScreen:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def draw_background(self):
        pass

    def draw_bird(self, bird_y: float, bird_vel: float):
        pass

    def draw_pipe(self, x, y_top, width):
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

    def show_frame(self):
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def draw_rect(self, color: tuple[int, int, int], rect: tuple[int, int, int, int]):
        pygame.draw.rect(self.screen, color, rect)


pygame.init()
