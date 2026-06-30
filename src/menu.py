import pygame

from src.button import Button


class Menu:
    def __init__(self, app):
        self.app = app
        self.buttons = {Button("start",300, 200, 200, 50, self.app.start_game)}
        self.clock = pygame.time.Clock()

    def handle_events(self, events):
        for event in events:
            for button in self.buttons:
                button.handle_event(event)

    def draw(self):
        self.app.screen.fill((20, 20, 20))
        for button in self.buttons:
            button.draw(self.app.screen)

    def run(self):
        while True:
            self.draw()
            self.handle_events(pygame.event.get())
            self.clock.tick(60)
            pygame.display.flip()