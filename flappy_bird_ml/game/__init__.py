from flappy_bird_ml.game.screen import GameScreenPyGame

if __name__ == "__main__":
    screen = GameScreenPyGame(288, 512)

    while True:
        screen.draw_background()
        screen.show_frame()
