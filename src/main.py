import pygame
from src.menu import Menu
from src.game import Game


WIDTH, HEIGHT = 800, 600


class App:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        pygame.mixer.init()
        pygame.mixer.music.load("../background.mp3")
        pygame.mixer.music.play(-1)
        self.volume = 0.3
        pygame.mixer.music.set_volume(self.volume)

        self.clock = pygame.time.Clock()

        self.running = True
        self.mode = "menu"

        self.menu = Menu(self)
        self.game = Game(self)

    def run(self):
        while self.running:

            dt = self.clock.tick(60) / 1000

            events = pygame.event.get()
            keys = pygame.key.get_pressed()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            if self.mode == "menu":
                self.menu.handle_events(events)
                self.menu.draw()

            elif self.mode == "game":
                self.game.handle_events(events)
                self.game.handle_keys(keys)

                self.game.update(dt)
                self.game.draw()

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    App().run()
