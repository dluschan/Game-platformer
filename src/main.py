import pygame
from src.menu import Menu
from src.game import Game


WIDTH, HEIGHT = 800, 600


class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game = Game(self.screen)
        self.menu = Menu(self)
        self.state = "menu"
        pygame.init()

    def run(self):
        if self.state == "game":
            self.game.run()
        elif self.state == "menu":
            self.menu.run()

    def start_game(self):
        self.state = "game"
        self.run()

if __name__ == "__main__":
    App().run()
