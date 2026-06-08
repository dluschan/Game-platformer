import pygame


class FlyingEnemy:
    def __init__(self, img_file_name, width, height, scale, frames, start_x, start_y, animation_speed, track):
        self.player_image = pygame.image.load(img_file_name).convert_alpha()
        self.player_image = pygame.transform.scale_by(self.player_image, scale)
        self.frames = frames
        self.animation_timer = 0
        self.animation_speed = animation_speed
        self.track = track

        self.player_frames = []
        for i in range(frames):
            frame = self.player_image.subsurface(pygame.Rect(i * width * scale, 0, width * scale, height * scale))
            self.player_frames.append(frame)

        self.player_current_frame = 0
        self.enemy_target_index = 0

        self.rect = pygame.Rect(start_x, start_y, width * scale, height * scale)
        self.speed = 5

    def __str__(self):
        return '\n'.join(f'{k} = {repr(v)}' for k, v in self.__dict__.items())

    def fly(self):
        target_x, target_y = self.track[self.enemy_target_index]
        dx = target_x - self.rect.x
        dy = target_y - self.rect.y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        if dist != 0:
            self.rect.x += dx / dist * self.speed
            self.rect.y += dy / dist * self.speed

        if dist < self.speed:
            self.enemy_target_index = (self.enemy_target_index + 1) % len(self.track)

    def get_frame(self):
        # TODO pygame.transform.flip
        return self.player_frames[self.player_current_frame]

    def next_frame(self):
        self.player_current_frame = (self.player_current_frame + 1) % self.frames
