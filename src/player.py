import pygame


class Player:
    def __init__(self, img_file_name, width, height, scale, frames, start_x, start_y):
        self.player_image = pygame.image.load(img_file_name).convert_alpha()
        self.player_image = pygame.transform.scale_by(self.player_image, scale)
        self.frames = frames

        self.player_frames = []
        for i in range(frames):
            frame = self.player_image.subsurface(pygame.Rect(i * width * scale, 0, width * scale, height * scale))
            self.player_frames.append(frame)

        self.player_current_frame = 0

        self.rect = pygame.Rect(start_x, start_y, width * scale, height * scale)
        self.max_speed = 5
        self.current_speed = 0

    def go_left(self):
        self.current_speed = max(self.current_speed - 1, - self.max_speed)
        self.rect.x += self.current_speed

    def go_right(self):
        self.current_speed = min(self.current_speed + 1, self.max_speed)
        self.rect.x += self.current_speed

    def go_by_inertia(self):
        if self.current_speed > 0:
            self.current_speed -= 1
        else:
            self.current_speed += 1
        self.rect.x += self.current_speed

    def get_speed(self):
        return self.current_speed

    def get_frame(self):
        # TODO pygame.transform.flip
        return self.player_frames[self.player_current_frame]

    def next_frame(self):
        # TODO if not moving: player_current_frame = 0
        self.player_current_frame = (self.player_current_frame + 1) % self.frames
