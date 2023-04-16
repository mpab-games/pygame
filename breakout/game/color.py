#SCREEN_COLOR = (249, 251, 255) # paper white
SCREEN_COLOR = (0, 0, 64)

BALL_BORDER_COLOR = (255, 0, 0)
BALL_FILL_COLOR = (192, 0, 0)
BAT_BORDER_COLOR = (0, 128, 0)
BAT_FILL_COLOR = (64, 192, 64)

BRICK_FILL_COLOR = (128, 128, 192)

class Gradient():
    def __init__(self, start, end):
        self.start = start
        self.end = end

BRIGHTGREEN_TO_MIDGREEN_GRADIENT = Gradient((64, 255, 64, 255), (0, 128, 0, 255))
MIDBLUE_TO_LIGHTBLUE_GRADIENT = Gradient((64, 64, 255, 255), (224, 224, 255, 255))
RED_TO_ORANGE_GRADIENT = Gradient((255, 0, 0, 255), (192, 192, 0, 255))
BRIGHTYELLOW_TO_MIDYELLOW_GRADIENT = Gradient((255, 255, 0, 255), (192, 192, 0, 255))

ORANGE_TO_GOLD_GRADIENT = Gradient((255, 140, 0, 255), (255, 215, 0, 255))
GOLD_TO_ORANGE_GRADIENT = Gradient((255, 215, 0, 255), (255, 140, 0, 255))

silver = (192, 192, 192)
red = (255, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
magenta = (255, 0, 255)
green = (0, 255, 0)
