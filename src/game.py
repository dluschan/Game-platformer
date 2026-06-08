import pygame
from level import levels
from src.player import Player

WIDTH, HEIGHT = 800, 600
ENEMY_SCALE = 2
FRAME_ENEMY_WIDTH = 20 * ENEMY_SCALE
FRAME_ENEMY_HEIGHT = 32 * ENEMY_SCALE
ENEMY_FRAMES = 2
ANIMATION_SPEED = 36
gravity = 0.55
low_gravity = 0.34
CAMERA_MARGIN = WIDTH * 0.4  # зона покоя

def show_message(surface, text, duration=1000):
    message = pygame.font.SysFont(None, 72).render(text, True, (255, 255, 255))
    rect = message.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))

    surface.fill((0, 0, 0))
    surface.blit(message, rect)
    pygame.display.flip()
    pygame.time.delay(duration)  # задержка в миллисекундах


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        pygame.mixer.music.load("../background.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background = pygame.image.load("../background.png").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.lives = 4
        self.player = Player("../person.png", 27, 48, 1.5, 3, 100, 100)

        self.running = True
        self.levels = levels
        self.current_level = 0
        self.level = self.levels[self.current_level]
        self.current_level = 0
        self.running_enemy_vel_y = 0
        self.jump_held = False

        self.debug = False

        self.enemy_image = pygame.image.load("../enemy.png").convert_alpha()
        self.enemy_image = pygame.transform.scale_by(self.enemy_image, ENEMY_SCALE)
        self.jump_sound = pygame.mixer.Sound("../jump.wav")
        self.hit_sound = pygame.mixer.Sound("../hit.wav")
        self.win_sound = pygame.mixer.Sound("../win.wav")

        self.enemy_frames = []
        for i in range(ENEMY_FRAMES):
            frame = self.enemy_image.subsurface(pygame.Rect(i * FRAME_ENEMY_WIDTH, 0, FRAME_ENEMY_WIDTH, FRAME_ENEMY_HEIGHT))
            self.enemy_frames.append(frame)

        self.enemy_track = [(2000, 100), (1000, 300)]
        self.enemy = pygame.Rect(*self.enemy_track[0], FRAME_ENEMY_WIDTH, FRAME_ENEMY_HEIGHT)
        self.running_enemy = pygame.Rect(1900, 200, FRAME_ENEMY_WIDTH, FRAME_ENEMY_HEIGHT)
        self.enemy_target_index = 1

        self.enemy_current_frame = 0
        self.enemy_frame_image = self.enemy_frames[self.enemy_current_frame]
        self.animation_timer = 0
        self.vel_y = 0
        self.can_jump = False
        self.jump_held = False
        self.enemy_speed = 5
        self.camera_x = 0

    def resolve_player_horizontal_collisions(self):
        for rect in self.level.ground + self.level.platforms:
            if self.player.rect.colliderect(rect):
                self.player.horizontal_hit(rect)

    def resolve_player_vertical_collisions(self):
        for rect in self.level.ground + self.level.platforms:
            if self.player.rect.colliderect(rect):
                self.player.vertical_hit(rect)
                break
        else:
            self.player.fly()

    def resolve_player_enemies_collisions(self):
        for enemy in self.level.obstacles + [self.enemy, self.running_enemy]:
            if self.player.rect.colliderect(enemy):
                self.lives -= 1
                self.hit_sound.play()
                self.player.rect.x = self.level.start_x
                self.player.rect.y = self.level.start_y
                if self.lives != 0:
                    show_message(self.screen, "CRASH!!!")
                else:
                    self.hit_sound.play()
                    show_message(self.screen, "GAME OVER!!!")
                    self.running = False

    def resolve_player_finish_collisions(self):
        if self.player.rect.colliderect(self.level.finish_platform):
            self.win_sound.play()
            show_message(self.screen, "WIN!", 1700)
            self.current_level = (self.current_level + 1) % len(self.levels)
            self.level = self.levels[self.current_level]
            self.player.rect.x = self.level.start_x
            self.player.rect.y = self.level.start_y
            self.vel_y = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                    self.jump_held = True
                    self.jump_sound.play()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.jump_held = False

                if event.key == pygame.K_LEFT:
                    self.player.stop()

                if event.key == pygame.K_RIGHT:
                    self.player.stop()

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.go_left()

        if keys[pygame.K_RIGHT]:
            self.player.go_right()

    def run(self):
        try:
            while self.running:
                self.handle_events()
                self.handle_keys()

                self.resolve_player_enemies_collisions()
                self.resolve_player_finish_collisions()

                self.player.apply_gravity(low_gravity if self.jump_held else gravity)

                self.player.vertical_update()
                self.resolve_player_vertical_collisions()

                self.player.horizontal_update()
                self.resolve_player_horizontal_collisions()

                left_border = self.camera_x + CAMERA_MARGIN
                right_border = self.camera_x + WIDTH - CAMERA_MARGIN

                if self.player.rect.x < left_border:
                    self.camera_x -= left_border - self.player.rect.x
                elif self.player.rect.x > right_border:
                    self.camera_x += self.player.rect.x - right_border

                # ограничение камеры границами уровня
                self.camera_x = max(0, min(self.camera_x, self.level.width - WIDTH))

                self.animation_timer += 1
                if self.animation_timer >= ANIMATION_SPEED:
                    self.animation_timer = 0
                    self.enemy_current_frame = (self.enemy_current_frame + 1) % ENEMY_FRAMES

                self.enemy_frame_image = self.enemy_frames[self.enemy_current_frame]
                self.enemy_frame_image = pygame.transform.flip(self.enemy_frame_image, True, False)
                target_x, target_y = self.enemy_track[self.enemy_target_index]
                dx = target_x - self.enemy.x
                dy = target_y - self.enemy.y
                dist = (dx ** 2 + dy ** 2) ** 0.5
                if dist != 0:
                    self.enemy.x += dx / dist * self.enemy_speed
                    self.enemy.y += dy / dist * self.enemy_speed

                if dist < self.enemy_speed:
                    self.enemy_target_index = (self.enemy_target_index + 1) % len(self.enemy_track)

                running_enemy_on_ground = False
                for ground in self.level.ground:
                    if self.running_enemy.colliderect(ground):
                        self.running_enemy.y = ground.top - self.running_enemy.height
                        running_enemy_on_ground = True

                running_enemy_on_platform = False
                for platform in self.level.platforms:
                    if self.running_enemy.colliderect(platform):
                        if self.running_enemy.colliderect(platform.left + 5, platform.top, platform.width - 10, 1):
                            self.running_enemy.y = platform.top - self.running_enemy.height
                            running_enemy_on_platform = True
                        elif self.running_enemy.colliderect(platform.left + 5, platform.bottom, platform.width - 10, 1):
                            self.running_enemy.y = platform.bottom
                        elif self.running_enemy.colliderect(platform.left, platform.top, 1, platform.height):
                            self.running_enemy.x = platform.left - self.running_enemy.width
                        elif self.running_enemy.colliderect(platform.right, platform.top, 1, platform.height):
                            self.running_enemy.x = platform.right
                running_enemy_can_jump = running_enemy_on_platform or running_enemy_on_ground

                self.running_enemy.x -= self.enemy_speed
                if not running_enemy_can_jump:
                    self.running_enemy_vel_y += gravity
                else:
                    self.running_enemy_vel_y = 0
                self.running_enemy.y += self.running_enemy_vel_y

                for obstacle in self.levels[self.current_level].obstacles:
                    if self.running_enemy.colliderect(obstacle):
                        self.running_enemy.x, self.running_enemy.y = 1900, 200

                self.screen.fill((0, 0, 0))
                self.screen.blit(self.background, (-self.camera_x * 0.3, 0))

                if self.debug:
                    lines = str(self.player).split('\n')
                    for i, line in enumerate(lines):
                        text = pygame.font.SysFont(None, 24).render(line, True, (255, 255, 255))
                        self.screen.blit(text, (10, 10 + i * 20))

                lives_text = pygame.font.SysFont(None, 32).render(f"Lives: {self.lives}", True, (255, 255, 255))
                self.screen.blit(lives_text, (10, 10))
                for obstacle in self.level.obstacles:
                    pygame.draw.rect(self.screen, (200, 10, 20), obstacle.move(-self.camera_x, 0))
                for ground in self.level.ground:
                    pygame.draw.rect(self.screen, (200, 200, 200), ground.move(-self.camera_x, 0))
                pygame.draw.rect(self.screen, (159, 10, 100), self.level.finish_platform.move(-self.camera_x, 0))
                for platform in self.level.platforms:
                    pygame.draw.rect(self.screen, (100, 255, 100), platform.move(-self.camera_x, 0))
                self.screen.blit(self.player.get_frame(), (self.player.rect.x - self.camera_x, self.player.rect.y))
                self.screen.blit(self.enemy_frame_image, (self.enemy.x - self.camera_x, self.enemy.y))
                self.screen.blit(self.enemy_frame_image, (self.running_enemy.x - self.camera_x, self.running_enemy.y))
                pygame.display.flip()
                self.clock.tick(60)
        finally:
            pygame.quit()

