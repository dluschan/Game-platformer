from pygame import Rect


class Platform:
    def __init__(self, left, top, width, height):
        self.rect = Rect(left, top, width, height)
