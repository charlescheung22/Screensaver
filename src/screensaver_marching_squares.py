# Here I attempt to implement a meta-balls-like screensaver by using the Marching Squares algorithm.


# relevant link for drawing circles with transparency:
# https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangles-and-polygons-in-pygame


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


class SpriteCircle(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int] | pygame.Vector2, radius: int,
                 direction: tuple[int, int] | pygame.Vector2, color: tuple[int, int, int]) -> None:
        """
        Circle class constructor.

        :param position: A tuple pair of coordinates, which will be converted to a vector.
        :param radius: Radius of the circle.
        :param direction: A tuple pair of coordinates, which will be converted to a vector.
        :param color: Color of the circle.
        """
        super().__init__()
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


class SpriteGridCircle(pygame.sprite.Sprite):
    def __init__(self, position: tuple[int, int] | pygame.Vector2, radius: int,
                 color: tuple[int, int, int] | tuple[int, int, int, int]) -> None:
        """
        Circle class constructor.

        :param position: A tuple pair of coordinates, which will be converted to a vector.
        :param radius: Radius of the circle.
        :param color: Color of the circle.
        """
        super().__init__()

        self.position = pygame.Vector2(position)
        self.radius = radius
        self.color = pygame.Color(color)

        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.set_colorkey((0, 0, 0))
        self.image.set_alpha(self.color.a)
        self.image.fill((0, 0, 0))
        pygame.draw.circle(self.image, self.color, self.position, self.radius)

        self.rect = self.image.get_rect(center=self.position)

    def update(self) -> None:
        pass


class GroupCircles(pygame.sprite.Group):
    def __init__(self, *sprites: SpriteCircle) -> None:
        """
        GroupCircles class constructor.

        :param sprites: A list of SpriteCircle objects.
        """
        super().__init__(self, *sprites)

    def update(self) -> None:
        """
        Update all the circles in the group.
        """
        for sprite in self.sprites():
            sprite.update()


class GroupContours(pygame.sprite.Group):
    def __init__(self, *sprites: SpriteCircle) -> None:
        """
        GroupContours class constructor.

        :param sprites: A list of SpriteCircle objects.
        """
        super().__init__(self, *sprites)

    def update(self) -> None:
        """
        Update all the contours in the group.
        """
        for sprite in self.sprites():
            sprite.update()


class GroupGridCircles(pygame.sprite.RenderPlain):
    def __init__(self, *sprites: SpriteCircle) -> None:
        """
        GroupGridCircles class constructor.

        :param sprites: A list of SpriteCircle objects.
        """
        super().__init__(self, *sprites)

    def update(self) -> None:
        """
        Update all the grid circles in the group.
        """
        for sprite in self.sprites():
            sprite.update()



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
    group_circles = GroupCircles()
    group_grid_circles = GroupGridCircles()
    group_contours = GroupContours()


    # set up a basic example grid of random values
    for x in range(SCREEN_WIDTH // RESOLUTION + 1):
        for y in range(SCREEN_HEIGHT // RESOLUTION + 1):
            # create a circle at the center of each grid cell
            grid_circle = SpriteGridCircle((x * RESOLUTION, y * RESOLUTION), RESOLUTION // 5, (255, 255, 255, int(255 * random.random())))
            grid_circle.add(group_grid_circles)
    # grid: list[list[float]] = []
    # for x in range(SCREEN_WIDTH // RESOLUTION + 1):
    #     grid.append([])
    #     for y in range(SCREEN_HEIGHT // RESOLUTION + 1):
    #         grid[x].append(random.random())  # a float between 0 and 1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Start rendering
        # If some debug toggles are enabled, draw them (later)
        screen.fill(BACKGROUND_COLOR)

        if debug_draw_grid:
            group_grid_circles.draw(screen)

        if debug_draw_circles:
            group_circles.draw(screen)

        pygame.display.flip()
        dt = clock.tick(FPS) / 1000  # Amount of seconds between each loop.

    pygame.quit()


if __name__ == "__main__":
    main()
