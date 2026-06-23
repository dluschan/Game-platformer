import pygame
from level import levels
from src.enemy import FlyingEnemy
from src.player import Player

WIDTH, HEIGHT = 800, 600
CAMERA_MARGIN = WIDTH * 0.4  # зона покоя

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        pygame.mixer.music.load("../background.mp3")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)

        self.jump_sound = pygame.mixer.Sound("../jump.wav")
        self.hit_sound = pygame.mixer.Sound("../hit.wav")
        self.win_sound = pygame.mixer.Sound("../win.wav")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background = pygame.image.load("../background.png").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        player_image = pygame.transform.scale_by(pygame.image.load("../person.png").convert_alpha(), 1.5)
        player_frames = [player_image.subsurface(pygame.Rect(i * 27 * 1.5, 0, 27 * 1.5, 48 * 1.5)) for i in range(3)]

        flying_enemy_image = pygame.transform.scale_by(pygame.image.load("../enemy.png").convert_alpha(), 2)
        flying_enemy_frames = [flying_enemy_image.subsurface(pygame.Rect(i * 20 * 2, 0, 20 * 2, 32 * 2)) for i in range(2)]

        self.player = Player(player_frames, 100, 100, 36)
        self.flying_enemy = FlyingEnemy(flying_enemy_frames, 2000, 100, 36, [(2000, 100), (1000, 300)])

        self.clock = pygame.time.Clock()
        self.lives = 4
        self.running = True
        self.levels = levels
        self.current_level = 0
        self.debug = False

        self.restart_level()

    def restart_level(self):
        self.level = self.levels[self.current_level]
        self.player.respawn(self.level.start_x, self.level.start_y)
        self.enemy_target_index = 1

        self.animation_timer = 0
        self.jump_held = False
        self.camera_x = 0
        self.time_left = self.level.time_left

    def run(self):
        try:
            while self.running:
                self.handle_events()
                self.handle_keys()

                self.resolve_player_enemies_collisions()
                self.resolve_player_finish_collisions()

                # TODO low gravity while falling if space keydown
                self.player.apply_gravity(self.level.low_gravity if self.jump_held else self.level.gravity)

                self.player.vertical_update()
                self.resolve_player_vertical_collisions()

                self.player.horizontal_update()
                self.resolve_player_horizontal_collisions()

                self.update_camera()

                self.flying_enemy.fly()

                self.update_time()
                self.draw()
        finally:
            pygame.quit()

    def update_time(self):
        self.time_left -= self.clock.tick(60) / 1000
        if self.time_left <= 0:
            self.player_death("TIME OUT")

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (-self.camera_x * 0.3, 0))

        if self.debug:
            lines = str(self.player).split('\n')
            for i, line in enumerate(lines):
                text = pygame.font.SysFont(None, 24).render(line, True, (255, 255, 255))
                self.screen.blit(text, (10, 10 + i * 20))

        lives_text = pygame.font.SysFont(None, 32).render(f"Lives: {self.lives}", True, (255, 255, 255))
        time_left_text = pygame.font.SysFont(None, 32).render(f"Time Left:{self.time_left}", True, (255, 255, 255))
        self.screen.blit(lives_text, (10, 10))
        self.screen.blit(time_left_text, (10, 45))
        for obstacle in self.level.obstacles:
            pygame.draw.rect(self.screen, (200, 10, 20), obstacle.move(-self.camera_x, 0))
        for ground in self.level.ground:
            pygame.draw.rect(self.screen, (200, 200, 200), ground.move(-self.camera_x, 0))
        pygame.draw.rect(self.screen, (159, 10, 100), self.level.finish_platform.move(-self.camera_x, 0))
        for platform in self.level.platforms:
            pygame.draw.rect(self.screen, (100, 255, 100), platform.move(-self.camera_x, 0))
        self.screen.blit(self.player.get_frame(), (self.player.rect.x - self.camera_x, self.player.rect.y))
        self.screen.blit(self.flying_enemy.get_frame(),
                         (self.flying_enemy.rect.x - self.camera_x, self.flying_enemy.rect.y))
        pygame.display.flip()

    def show_message(self, text, duration=1000):
        message = pygame.font.SysFont(None, 72).render(text, True, (255, 255, 255))
        rect = message.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        self.screen.fill((0, 0, 0))
        self.screen.blit(message, rect)
        pygame.display.flip()
        pygame.time.delay(duration)  # задержка в миллисекундах

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
        for enemy in self.level.obstacles + [self.flying_enemy]:
            if self.player.rect.colliderect(enemy):
                self.player_death("CRASH")

    def player_death(self, message):
        self.hit_sound.play()
        self.lives -= 1
        if self.lives != 0:
            self.show_message(message)
        else:
            self.show_message("GAME OVER!!!")
            self.running = False
        self.restart_level()

    def resolve_player_finish_collisions(self):
        if self.player.rect.colliderect(self.level.finish_platform):
            self.win_sound.play()
            self.show_message("WIN!", 1700)
            self.current_level = (self.current_level + 1) % len(self.levels)
            self.restart_level()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.player.jump():
                        self.jump_held = True
                        self.jump_sound.play()

                if event.key == pygame.K_d:
                    self.debug = not self.debug

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
            self.player.left()

        if keys[pygame.K_RIGHT]:
            self.player.right()

    def update_camera(self):
        left_border = self.camera_x + CAMERA_MARGIN
        right_border = self.camera_x + WIDTH - CAMERA_MARGIN

        if self.player.rect.x < left_border:
            self.camera_x -= left_border - self.player.rect.x
        elif self.player.rect.x > right_border:
            self.camera_x += self.player.rect.x - right_border

        # ограничение камеры границами уровня
        self.camera_x = max(0, min(self.camera_x, self.level.width - WIDTH))

