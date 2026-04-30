import pygame
from pygame import font


class Level:
    def __init__(self, width, start_x, start_y, platforms, finish_platform, ground, obstacles):
        self.width = width
        self.start_x = start_x
        self.start_y = start_y
        self.platforms = platforms
        self.finish_platform = finish_platform
        self.ground = ground
        self.obstacles = obstacles


def show_message(surface, text, duration=1000):
    font = pygame.font.SysFont(None, 72)
    message = font.render(text, True, (255, 255, 255))
    rect = message.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))

    surface.fill((0, 0, 0))
    surface.blit(message, rect)
    pygame.display.flip()
    pygame.time.delay(duration)  # задержка в миллисекундах


pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("background.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

WIDTH, HEIGHT = 800, 600
clock = pygame.time.Clock()
lives = 4

level_0 = Level(width = 8000,
    start_x = 100,
    start_y = 100,
    platforms = [
        pygame.Rect(600, 450, 120, 10),
        pygame.Rect(850, 350, 120, 10),
        pygame.Rect(1010, 240, 120, 10),
        pygame.Rect(1260, 400, 120, 10),
        pygame.Rect(1480, 230, 120, 10),
        pygame.Rect(1740, 300, 120, 10),
        pygame.Rect(1940, 360, 120, 10),
        pygame.Rect(2350 , 580, 150, 10),
        pygame.Rect(2630 , 470, 120, 10),
        pygame.Rect(2860, 350, 120, 10),
        pygame.Rect(3100, 280, 120, 10),
        pygame.Rect(3400, 200, 120, 10),
        pygame.Rect(3650, 350, 120, 10),
        pygame.Rect(3990, 200, 120, 10),
        pygame.Rect(4190, 310, 120, 10),
        pygame.Rect(4480, 420, 120, 10),
        pygame.Rect(4780, 250, 120, 10),
        pygame.Rect(5020, 100, 120, 10),
        pygame.Rect(5280, 300, 120, 10),
        pygame.Rect(5700, 270, 120, 10),
        pygame.Rect(6120, 550, 210, 10),
        pygame.Rect(6480, 360, 120, 10),
        pygame.Rect(6750, 200, 120, 10),
        pygame.Rect(7090, 270, 120, 10),
        pygame.Rect(7090, 270, 120, 10),
        pygame.Rect(7090, 270, 120, 10),
        pygame.Rect(7490, 400, 120, 10),
    ],
    finish_platform = pygame.Rect(7860, 450, 140, 10),
    ground = pygame.Rect(0, 550, 600, 50),
    obstacles = [
        pygame.Rect(420, 350, 100, 10),
        pygame.Rect(1600, 150, 100, 10),
        pygame.Rect(600, 700, 8400, 10),
        pygame.Rect(2270, 350, 10, 120),
        pygame.Rect(3820, 270, 10, 120),
        pygame.Rect(600, 700, 3400, 10),
        pygame.Rect(5480, 250, 10, 100),
        pygame.Rect(5980, 130, 10, 100),

    ]
              )

levels = [level_0, level_0]
current_level = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, (levels[current_level].width, HEIGHT))  # растянуть под уровень

PLAYER_SCALE = 1.5
ENEMY_SCALE = 2
FRAME_PLAYER_WIDTH = 27 * PLAYER_SCALE
FRAME_PLAYER_HEIGHT = 48 * PLAYER_SCALE
FRAME_ENEMY_WIDTH = 20 * ENEMY_SCALE
FRAME_ENEMY_HEIGHT = 32 * ENEMY_SCALE
PLAYER_FRAMES = 3
ENEMY_FRAMES = 2


player_image = pygame.image.load("person.png").convert_alpha()
player_image = pygame.transform.scale_by(player_image, PLAYER_SCALE)
enemy_image = pygame.image.load("enemy.png").convert_alpha()
enemy_image = pygame.transform.scale_by(enemy_image, ENEMY_SCALE)
jump_sound = pygame.mixer.Sound("jump.wav")
hit_sound  = pygame.mixer.Sound("hit.wav")
win_sound = pygame.mixer.Sound("win.wav")

player_frames = []
for i in range( PLAYER_FRAMES):
    frame = player_image.subsurface(pygame.Rect(i * FRAME_PLAYER_WIDTH, 0, FRAME_PLAYER_WIDTH, FRAME_PLAYER_HEIGHT))
    player_frames.append(frame)

player = pygame.Rect(levels[current_level].start_x, levels[current_level].start_y, FRAME_PLAYER_WIDTH, FRAME_PLAYER_HEIGHT)

enemy_frames = []
for i in range(ENEMY_FRAMES):
    frame = enemy_image.subsurface(pygame.Rect(i * FRAME_ENEMY_WIDTH, 0, FRAME_ENEMY_WIDTH, FRAME_ENEMY_HEIGHT))
    enemy_frames.append(frame)

enemy = pygame.Rect(300,350, FRAME_ENEMY_WIDTH, FRAME_ENEMY_HEIGHT)

player_current_frame = 0
enemy_current_frame = 0
player_frame_image = player_frames[player_current_frame]
enemy_frame_image = enemy_frames[enemy_current_frame]
animation_timer = 0
ANIMATION_SPEED = 36
vel_y = 0
gravity = 0.55
low_gravity = 0.34
can_jump = False
jump_held = False
MIN_SPEED, MAX_SPEED = 5, 8
speed = MIN_SPEED
camera_x = 0
CAMERA_MARGIN = WIDTH * 0.4  # зона покоя

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if can_jump:
                    vel_y = -12
                    can_jump = False
                    jump_held = True
                    jump_sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                if not can_jump:
                    jump_held = False


    keys = pygame.key.get_pressed()
    moving = False
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= speed
        player_frame_image = player_frames[player_current_frame]
        player_frame_image = pygame.transform.flip(player_frame_image, True, False)
        moving = True
    if keys[pygame.K_RIGHT] and player.right < levels[current_level].width:
        player.x += speed
        player_frame_image = player_frames[player_current_frame]
        moving = True

    if jump_held:
        vel_y += low_gravity
    else:
        vel_y += gravity
    player.y += vel_y
    on_ground = False
    if player.colliderect(levels[current_level].ground):
        player.y = levels[current_level].ground.top - player.height
        vel_y = 0
        on_ground = True

    if player.colliderect(enemy):
        lives -= 1
        player.x = levels[current_level].start_x
        player.y = levels[current_level].start_y
        if lives != 0:
            show_message(screen, "TOUCH!")
        else:
            hit_sound.play()
            show_message(screen, "GAME OVER!!!")
            running = False
    if player.colliderect(levels[current_level].finish_platform):
        player.y = levels[current_level].finish_platform.top - player.height
        vel_y = 0
        win_sound.play()
        show_message(screen,"WIN!", 1700)
        current_level = (current_level + 1) % len(levels)
        # running = False
    on_platform = False
    for platform in levels[current_level].platforms:
        if player.colliderect(platform):
            if player.colliderect(platform.left + 5, platform.top, platform.width - 10, 1):
                player.y = platform.top - player.height
                vel_y = 0
                on_platform = True
            elif player.colliderect(platform.left + 5, platform.bottom, platform.width - 10, 1):
                player.y = platform.bottom
                vel_y = 0

            elif player.colliderect(platform.left, platform.top, 1, platform.height):
                player.x = platform.left - player.width
            elif player.colliderect(platform.right, platform.top, 1, platform.height):
                player.x = platform.right
    can_jump = on_platform or on_ground
    for obstacle in levels[current_level].obstacles:
        if player.colliderect(obstacle):
            lives -= 1
            hit_sound.play()
            player.x = levels[current_level].start_x
            player.y = levels[current_level].start_y
            if lives != 0:
                show_message(screen, "CRASH!!!")
            else:
                hit_sound.play()
                show_message(screen, "GAME OVER!!!")
                running = False

    left_border = camera_x + CAMERA_MARGIN
    right_border = camera_x + WIDTH - CAMERA_MARGIN

    if player.x < left_border:
        camera_x -= left_border - player.x
    elif player.x > right_border:
        camera_x += player.x - right_border

    # ограничение камеры границами уровня
    camera_x = max(0, min(camera_x, levels[current_level].width - WIDTH))

    animation_timer += 1
    if animation_timer >= ANIMATION_SPEED:
        animation_timer = 0
        if moving:
            player_current_frame = (player_current_frame + 1) % PLAYER_FRAMES
        else:
            player_current_frame = 0

    screen.blit(background, (-camera_x * 0.3, 0))
    font = pygame.font.SysFont(None, 32)
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))
    for obstacle in levels[current_level].obstacles:
        pygame.draw.rect(screen, (200, 10, 20), obstacle.move(-camera_x, 0))
    pygame.draw.rect(screen, (200, 200, 200), levels[current_level].ground.move(-camera_x, 0))
    pygame.draw.rect(screen, (159, 10, 100), levels[current_level].finish_platform.move(-camera_x, 0))
    for platform in levels[current_level].platforms:
        pygame.draw.rect(screen, (100, 255, 100), platform.move(-camera_x, 0))
    screen.blit(player_frame_image, (player.x - camera_x, player.y))
    screen.blit(enemy_frame_image, (enemy.x, enemy.y))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
