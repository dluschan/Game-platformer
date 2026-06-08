import pygame

from src.game import Game
from src.level import Level
from src.player import Player


def show_message(surface, text, duration=1000):
    font = pygame.font.SysFont(None, 72)
    message = font.render(text, True, (255, 255, 255))
    rect = message.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))

    surface.fill((0, 0, 0))
    surface.blit(message, rect)
    pygame.display.flip()
    pygame.time.delay(duration)  # задержка в миллисекундах


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
    ground = [pygame.Rect(0, 550, 600, 50)],
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
level_1 = Level(width = 13000,
    start_x = 100,
    start_y = 100,
    platforms = [
        pygame.Rect(600, 450, 120, 10),
        pygame.Rect(850, 350, 120, 10),
        pygame.Rect(1010, 240, 120, 10),
        pygame.Rect(1260, 400, 120, 10),
        pygame.Rect(1480, 230, 120, 10),
        pygame.Rect(1740, 300, 120, 10),
    ],
    finish_platform = pygame.Rect(1860, 450, 140, 10),
    ground = [
        pygame.Rect(0, 550, 600, 50),
        pygame.Rect(800, 550, 1200, 50),
    ],
    obstacles = [
        pygame.Rect(420, 350, 100, 10),
        pygame.Rect(1600, 150, 100, 10),
        pygame.Rect(0, 700, 2000, 10),
        pygame.Rect(600, 700, 3400, 10),
    ]
)

levels = [level_0, level_1]
current_level = 0
running_enemy_vel_y = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load("../background.png").convert()
background = pygame.transform.scale(background, (levels[current_level].width, HEIGHT))  # растянуть под уровень

player = Player("../person.png", 27, 48, 1.5, 3, 100, 100)

ENEMY_SCALE = 2
FRAME_ENEMY_WIDTH = 20 * ENEMY_SCALE
FRAME_ENEMY_HEIGHT = 32 * ENEMY_SCALE
ENEMY_FRAMES = 2

game = Game()

enemy_image = pygame.image.load("../enemy.png").convert_alpha()
enemy_image = pygame.transform.scale_by(enemy_image, ENEMY_SCALE)
jump_sound = pygame.mixer.Sound("../jump.wav")
hit_sound  = pygame.mixer.Sound("../hit.wav")
win_sound = pygame.mixer.Sound("../win.wav")

enemy_frames = []
for i in range(ENEMY_FRAMES):
    frame = enemy_image.subsurface(pygame.Rect(i * FRAME_ENEMY_WIDTH, 0, FRAME_ENEMY_WIDTH, FRAME_ENEMY_HEIGHT))
    enemy_frames.append(frame)

enemy_track = [(2000, 100), (1000, 300)]
enemy = pygame.Rect(*enemy_track[0], FRAME_ENEMY_WIDTH, FRAME_ENEMY_HEIGHT)
running_enemy = pygame.Rect(1900, 200, FRAME_ENEMY_WIDTH, FRAME_ENEMY_HEIGHT)
enemy_target_index = 1

enemy_current_frame = 0
enemy_frame_image = enemy_frames[enemy_current_frame]
animation_timer = 0
ANIMATION_SPEED = 36
vel_y = 0
gravity = 0.55
low_gravity = 0.34
can_jump = False
jump_held = False
MIN_SPEED, MAX_SPEED = 5, 8
enemy_speed = 5

camera_x = 0
CAMERA_MARGIN = WIDTH * 0.4  # зона покоя

while game.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False

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
    if keys[pygame.K_LEFT] and player.rect.left > 0:
        player.go_left()
        moving = True
    if keys[pygame.K_RIGHT] and player.rect.right < levels[current_level].width:
        player.go_right()
        moving = True

    if moving == False and player.get_speed() != 0:
        player.go_by_inertia()

    if jump_held:
        vel_y += low_gravity
    else:
        vel_y += gravity
    player.rect.y += vel_y
    on_ground = False
    for ground in levels[current_level].ground:
        if player.rect.colliderect(ground):
            player.rect.y = ground.top - player.rect.height
            vel_y = 0
            on_ground = True

    if player.rect.colliderect(enemy) or player.rect.colliderect(running_enemy):
        lives -= 1
        player.rect.x = levels[current_level].start_x
        player.rect.y = levels[current_level].start_y
        if lives != 0:
            show_message(screen, "TOUCH!")
        else:
            hit_sound.play()
            show_message(screen, "GAME OVER!!!")
            game.running = False

    if player.rect.colliderect(levels[current_level].finish_platform):
        win_sound.play()
        show_message(screen,"WIN!", 1700)
        current_level = (current_level + 1) % len(levels)
        player.rect.x = levels[current_level].start_x
        player.rect.y = levels[current_level].start_y
        vel_y = 0

    on_platform = False
    for platform in levels[current_level].platforms:
        if player.rect.colliderect(platform):
            if player.rect.colliderect(platform.left + 5, platform.top, platform.width - 10, 1):
                player.rect.y = platform.top - player.rect.height
                vel_y = 0
                on_platform = True
            elif player.rect.colliderect(platform.left + 5, platform.bottom, platform.width - 10, 1):
                player.rect.y = platform.bottom
                vel_y = 0
            elif player.rect.colliderect(platform.left, platform.top, 1, platform.height):
                player.rect.x = platform.left - player.rect.width
            elif player.rect.colliderect(platform.right, platform.top, 1, platform.height):
                player.rect.x = platform.right
    can_jump = on_platform or on_ground

    for obstacle in levels[current_level].obstacles:
        if player.rect.colliderect(obstacle):
            lives -= 1
            hit_sound.play()
            player.rect.x = levels[current_level].start_x
            player.rect.y = levels[current_level].start_y
            if lives != 0:
                show_message(screen, "CRASH!!!")
            else:
                hit_sound.play()
                show_message(screen, "GAME OVER!!!")
                game.running = False

    left_border = camera_x + CAMERA_MARGIN
    right_border = camera_x + WIDTH - CAMERA_MARGIN

    if player.rect.x < left_border:
        camera_x -= left_border - player.rect.x
    elif player.rect.x > right_border:
        camera_x += player.rect.x - right_border

    # ограничение камеры границами уровня
    camera_x = max(0, min(camera_x, levels[current_level].width - WIDTH))

    animation_timer += 1
    if animation_timer >= ANIMATION_SPEED:
        animation_timer = 0
        enemy_current_frame = (enemy_current_frame + 1) % ENEMY_FRAMES
        if moving:
            player.next_frame()

    enemy_frame_image = enemy_frames[enemy_current_frame]
    enemy_frame_image = pygame.transform.flip(enemy_frame_image, True, False)
    target_x, target_y = enemy_track[enemy_target_index]
    dx = target_x - enemy.x
    dy = target_y - enemy.y
    dist = (dx**2 + dy**2) ** 0.5
    if dist != 0:
        enemy.x += dx / dist * enemy_speed
        enemy.y += dy / dist * enemy_speed

    if dist < enemy_speed:
        enemy_target_index = (enemy_target_index + 1) % len(enemy_track)

    running_enemy_on_ground = False
    for ground in levels[current_level].ground:
        if running_enemy.colliderect(ground):
            running_enemy.y = ground.top - running_enemy.height
            running_enemy_vel_y = 0
            running_enemy_on_ground = True

    running_enemy_on_platform = False
    for platform in levels[current_level].platforms:
        if running_enemy.colliderect(platform):
            if running_enemy.colliderect(platform.left + 5, platform.top, platform.width - 10, 1):
                running_enemy.y = platform.top - running_enemy.height
                running_enemy_on_platform = True
            elif running_enemy.colliderect(platform.left + 5, platform.bottom, platform.width - 10, 1):
                running_enemy.y = platform.bottom
            elif running_enemy.colliderect(platform.left, platform.top, 1, platform.height):
                running_enemy.x = platform.left - running_enemy.width
            elif running_enemy.colliderect(platform.right, platform.top, 1, platform.height):
                running_enemy.x = platform.right
    running_enemy_can_jump = running_enemy_on_platform or running_enemy_on_ground

    running_enemy.x -= enemy_speed
    if not running_enemy_can_jump:
        running_enemy_vel_y += gravity
    else:
        running_enemy_vel_y = 0
    running_enemy.y += running_enemy_vel_y

    for obstacle in levels[current_level].obstacles:
        if running_enemy.colliderect(obstacle):
            running_enemy.x, running_enemy.y = 1900, 200


    screen.blit(background, (-camera_x * 0.3, 0))
    font = pygame.font.SysFont(None, 32)
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))
    for obstacle in levels[current_level].obstacles:
        pygame.draw.rect(screen, (200, 10, 20), obstacle.move(-camera_x, 0))
    for ground in levels[current_level].ground:
        pygame.draw.rect(screen, (200, 200, 200), ground.move(-camera_x, 0))
    pygame.draw.rect(screen, (159, 10, 100), levels[current_level].finish_platform.move(-camera_x, 0))
    for platform in levels[current_level].platforms:
        pygame.draw.rect(screen, (100, 255, 100), platform.move(-camera_x, 0))
    screen.blit(player.get_frame(), (player.rect.x - camera_x, player.rect.y))
    screen.blit(enemy_frame_image, (enemy.x - camera_x, enemy.y))
    screen.blit(enemy_frame_image, (running_enemy.x - camera_x, running_enemy.y))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
