from dataclasses import field

import pygame


class Player:
    def __init__(self, img_file_name, width, height, scale, frames, start_x, start_y):
        self.player_image = pygame.image.load(img_file_name).convert_alpha()
        self.player_image = pygame.transform.scale_by(self.player_image, scale)
        self.frames = frames
        self.moving = False
        self.on_ground = False

        self.player_frames = []
        for i in range(frames):
            frame = self.player_image.subsurface(pygame.Rect(i * width * scale, 0, width * scale, height * scale))
            self.player_frames.append(frame)

        self.player_current_frame = 0

        self.rect = pygame.Rect(start_x, start_y, width * scale, height * scale)
        self.max_speed = 5
        self.velocity_x = 0
        self.velocity_y = 0

    def __str__(self):
        return '\n'.join(f'{k} = {repr(v)}' for k, v in self.__dict__.items())

    def apply_gravity(self, gravity):
        # if not self.on_ground:
        self.velocity_y += gravity

    def go_left(self):
        self.moving = True
        self.velocity_x = max(self.velocity_x - 1, - self.max_speed)

    def go_right(self):
        self.moving = True
        self.velocity_x = min(self.velocity_x + 1, self.max_speed)

    def stop(self):
        self.moving = False

    def vertical_hit(self, rect):
        if self.velocity_y > 0:
            self.land_on(rect)
        else:
            self.hit_ceiling(rect)

    def land_on(self, rect):
        self.rect.bottom = rect.top
        self.velocity_y = 0
        self.on_ground = True

    def hit_ceiling(self, rect):
        self.rect.top = rect.bottom
        self.velocity_y = 0

    def horizontal_hit(self, rect):
        if self.velocity_x > 0:
            self.rect.right = rect.left
        else:
            self.rect.left = rect.right

    def jump(self):
        if self.on_ground:
            self.on_ground = False
            self.velocity_y = -12

    def fly(self):
        self.on_ground = False

    def vertical_update(self):
        self.rect.y += self.velocity_y

    def horizontal_update(self):
        if not self.moving and self.velocity_x:
            self.go_by_inertia()
            self.next_frame()
        elif self.moving:
            self.next_frame()
        self.rect.x += self.velocity_x

    def go_by_inertia(self):
        if self.velocity_x > 0:
            self.velocity_x -= 1
        elif self.velocity_x < 0:
            self.velocity_x += 1

    def get_frame(self):
        # TODO pygame.transform.flip
        return self.player_frames[self.player_current_frame]

    def next_frame(self):
        # TODO if not moving: player_current_frame = 0
        self.player_current_frame = (self.player_current_frame + 1) % self.frames
