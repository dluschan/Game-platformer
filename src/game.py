import pygame


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        pygame.mixer.music.load("../background.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)

        self.running = True
