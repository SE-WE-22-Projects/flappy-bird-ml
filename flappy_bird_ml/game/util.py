from flappy_bird_ml.game import colors


def text_shadow(surface, txt, font, colour, x, y):
    shadow = font.render(txt, True, colors.DARK_GREY)
    surface.blit(shadow, (x + 2, y + 2))
    label = font.render(txt, True, colour)
    surface.blit(label, (x, y))
