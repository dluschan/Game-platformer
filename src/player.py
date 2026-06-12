import pygame


class Player:
    def __init__(self, frames, start_x, start_y, animation_speed):
        self.frames = frames
        self.x_force_active = False
        self.on_ground = False
        self.animation_timer = 0
        self.animation_speed = animation_speed
        self.player_current_frame = 0

        self.rect = pygame.Rect(start_x, start_y, self.frames[0].get_width(), self.frames[0].get_height())
        self.max_speed = 5
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_go_right = True

    def __str__(self):
        return '\n'.join(f'{k} = {repr(v)}' for k, v in self.__dict__.items())

    def apply_gravity(self, gravity):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.next_frame()
        self.velocity_y += gravity

    def left(self):
        self.x_force_active = True
        self.velocity_x = max(self.velocity_x - 1, - self.max_speed)
        self.is_go_right = False

    def right(self):
        self.x_force_active = True
        self.velocity_x = min(self.velocity_x + 1, self.max_speed)
        self.is_go_right = True

    def stop(self):
        self.x_force_active = False

    def respawn(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.velocity_x = 0
        self.velocity_y = 0

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
        if not self.x_force_active and self.velocity_x:
            self.go_by_inertia()
        self.rect.x += self.velocity_x

    def go_by_inertia(self):
        if self.velocity_x > 0:
            self.velocity_x -= 1
        elif self.velocity_x < 0:
            self.velocity_x += 1

    def get_frame(self):
        if self.is_go_right:
            return self.frames[self.player_current_frame]
        else:
            return pygame.transform.flip(self.frames[self.player_current_frame], True, False)


    def next_frame(self):
        if self.velocity_x and self.on_ground:
            self.player_current_frame = (self.player_current_frame + 1) % len(self.frames)
        else:
            self.player_current_frame = 0