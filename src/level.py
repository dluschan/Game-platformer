class Level:
    def __init__(self, width, start_x, start_y, platforms, finish_platform, ground, obstacles):
        self.width = width
        self.start_x = start_x
        self.start_y = start_y
        self.platforms = platforms
        self.finish_platform = finish_platform
        self.ground = ground
        self.obstacles = obstacles
