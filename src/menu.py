import pygame

from src.button import Button


class Menu:
    def __init__(self, app):
        self.app = app
        self.buttons = [
            Button("Start",300, 200, 200, 60, self.start_game),
            Button("Quit",300, 300, 200, 60, self.quit)
        ]

    def handle_events(self, events):
        for event in events:
            for button in self.buttons:
                button.handle_event(event)

    def draw(self):
        self.app.screen.fill((20, 20, 20))
        for button in self.buttons:
            button.draw(self.app.screen)

    def start_game(self):
        self.app.mode = "game"
        self.app.game.start()

    def quit(self):
        self.app.running = False