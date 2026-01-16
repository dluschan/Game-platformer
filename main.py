import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = pygame.Rect(100, 100, 40, 60)
platform = pygame.Rect(300, 450, 100, 10)
vel_y = 0
gravity = 0.5
speed = 5
obstacle = pygame.Rect(420, 350, 100, 10)
ground = pygame.Rect(0, 550, 800, 50)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed
    if keys[pygame.K_SPACE] and player.y == ground.top - player.height:
        vel_y = -12
    if keys[pygame.K_SPACE] and player.y == platform.top - player.height:
        vel_y = -12

    vel_y += gravity
    player.y += vel_y

    if player.colliderect(ground):
        player.y = ground.top - player.height
        vel_y = 0

    if player.colliderect(platform):
        if player.colliderect(platform.left + 5, platform.top, platform.width - 10, 1):
            player.y = platform.top - player.height
            vel_y = 0
        elif player.colliderect(platform.left + 5, platform.bottom, platform.width - 10, 1):
            player.y = platform.bottom
            vel_y = 0
        elif player.colliderect(platform.left, platform.top, 1, platform.height):
            player.x = platform.left - player.width
        elif player.colliderect(platform.right, platform.top, 1, platform.height):
            player.x = platform.right
    if player.colliderect(obstacle):
        running = False
    screen.fill((30, 30, 30))
    pygame.draw.rect(screen, (200, 200, 200), ground)
    pygame.draw.rect(screen, (100, 180, 255), player)
    pygame.draw.rect(screen, (100, 255, 100), platform)
    pygame.draw.rect(screen, (200, 10, 20), obstacle )
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
