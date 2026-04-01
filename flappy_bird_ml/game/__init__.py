from flappy_bird_ml.game.screen import GameScreenPyGame
from flappy_bird_ml.game.state import Bird, Pipe

if __name__ == "__main__":
    screen = GameScreenPyGame(288, 512)

    while True:
        screen.draw_background()
        screen.draw_bird(Bird(60, 10))
        screen.draw_pipe(Pipe(120, 40))
        screen.show_frame()
