from pygame import Rect


class Level:
    def __init__(self, width, start_x, start_y, gravity, low_gravity, platforms, finish_platform, ground, obstacles):
        self.width = width
        self.start_x = start_x
        self.start_y = start_y
        self.gravity = gravity
        self.low_gravity = low_gravity
        self.platforms = platforms
        self.finish_platform = finish_platform
        self.ground = ground
        self.obstacles = obstacles

levels = [
    Level(
        width = 8000,
        start_x = 100,
        start_y = 100,
        gravity = 0.55,
        low_gravity = 0.34,
        platforms = [
            Rect(600, 450, 120, 10),
            Rect(850, 350, 120, 10),
            Rect(1010, 240, 120, 10),
            Rect(1260, 400, 120, 10),
            Rect(1480, 230, 120, 10),
            Rect(1740, 300, 120, 10),
            Rect(1940, 360, 120, 10),
            Rect(2350 , 580, 150, 10),
            Rect(2630 , 470, 120, 10),
            Rect(2860, 350, 120, 10),
            Rect(3100, 280, 120, 10),
            Rect(3400, 200, 120, 10),
            Rect(3650, 350, 120, 10),
            Rect(3990, 200, 120, 10),
            Rect(4190, 310, 120, 10),
            Rect(4480, 420, 120, 10),
            Rect(4780, 250, 120, 10),
            Rect(5020, 100, 120, 10),
            Rect(5280, 300, 120, 10),
            Rect(5700, 270, 120, 10),
            Rect(6120, 550, 210, 10),
            Rect(6480, 360, 120, 10),
            Rect(6750, 200, 120, 10),
            Rect(7090, 270, 120, 10),
            Rect(7090, 270, 120, 10),
            Rect(7090, 270, 120, 10),
            Rect(7490, 400, 120, 10),
        ],
        finish_platform = Rect(7860, 450, 140, 10),
        ground = [Rect(0, 550, 600, 50)],
        obstacles = [
            Rect(420, 350, 100, 10),
            Rect(1600, 150, 100, 10),
            Rect(600, 700, 8400, 10),
            Rect(2270, 350, 10, 120),
            Rect(3820, 270, 10, 120),
            Rect(600, 700, 3400, 10),
            Rect(5480, 250, 10, 100),
            Rect(5980, 130, 10, 100),
        ]
    ),
    Level(
        width = 13000,
        start_x = 100,
        start_y = 100,
        gravity = 0.55,
        low_gravity = 0.34,
        platforms = [
            Rect(600, 450, 120, 10),
            Rect(850, 350, 120, 10),
            Rect(1010, 240, 120, 10),
            Rect(1260, 400, 120, 10),
            Rect(1480, 230, 120, 10),
            Rect(1740, 300, 120, 10),
        ],
        finish_platform = Rect(1860, 450, 140, 10),
        ground = [
            Rect(0, 550, 600, 50),
            Rect(800, 550, 1200, 50),
        ],
        obstacles = [
            Rect(420, 350, 100, 10),
            Rect(1600, 150, 100, 10),
            Rect(0, 700, 2000, 10),
            Rect(600, 700, 3400, 10),
        ]
    )
]
