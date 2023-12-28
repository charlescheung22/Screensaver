# Here I attempt to implement a meta-balls-like screensaver by using the Marching Squares algorithm.

import pygame
import random

FPS = 60
FULLSCREEN = False
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
SCREEN_SIZE: tuple[int, int] = (SCREEN_WIDTH, SCREEN_HEIGHT)
RESOLUTION: int = 20  # resolution value is a denominator value, so higher val means less display resolution
BACKGROUND_COLOR: tuple[int, int, int] = (0, 0, 0)
BALL_COLOR: tuple[int, int, int] = (255, 0, 0)

debug_draw_grid = True
debug_draw_circles = True


class Circle(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int] | pygame.Vector2, radius: int,
                 direction: tuple[int, int] | pygame.Vector2, color: tuple[int, int, int]) -> None:
        """
        Circle class constructor.

        :param position: A tuple pair of coordinates, which will be converted to a vector.
        :param radius: Radius of the circle.
        :param direction: A tuple pair of coordinates, which will be converted to a vector.
        :param color: Color of the circle.
        """
        pygame.sprite.Sprite.__init__(self)  # or just super().__init__()

        self.position = pygame.Vector2(position)
        self.radius = radius
        self.direction = pygame.Vector2(direction)
        self.color = color

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the circle on a given surface.

        :param surface: Pygame surface to draw the circle on.
        """
        pygame.draw.circle(surface, self.color, self.position, self.radius)

    def update(self) -> None:
        pass


def main():
    # Initialize pygame and some other stuff
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    if FULLSCREEN:
        pygame.display.toggle_fullscreen()
    clock = pygame.time.Clock()
    delta_time = 0  # Time since last frame in seconds, needed for time independent physics
    running = True

    # Use the group and sprite functionality of pygame
    group_circles = pygame.sprite.Group()

    # set up some grid stuff
    grid: list[list[float]] = []
    for x in range(SCREEN_WIDTH // RESOLUTION):
        grid.append([])
        for y in range(SCREEN_HEIGHT // RESOLUTION):
            grid[x].append(random.random())  # a float between 0 and 1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Start rendering
        # If some debug toggles are enabled, draw them (later)
        screen.fill(BACKGROUND_COLOR)

        if debug_draw_grid:
            for x in range(SCREEN_WIDTH // RESOLUTION):
                for y in range(SCREEN_HEIGHT // RESOLUTION):
                    # use the grid value as a transparency value (alpha in RGBa)
                    temp = pygame.Color(255, 255, 255, int(255 * grid[x][y]))
                    pygame.draw.circle(screen, temp,
                                       (x * RESOLUTION, y * RESOLUTION), RESOLUTION // 5)

        if debug_draw_circles:
            group_circles.draw(screen)

        pygame.display.flip()
        dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop.

    pygame.quit()


if __name__ == "__main__":
    main()
