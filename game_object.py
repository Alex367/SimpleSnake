import random
import enum
import pygame

min_coord = 100
max_coord = 450
black = 0, 0, 0
green = 0, 255, 0
red = 225, 0, 0
purple = 218, 112, 214
yellow = 240, 230, 140
size = width, height = 600, 600
field_width = field_height = 500
left_margin_field = top_margin_field = 50

# food
cnt_food = 3
# wall
cnt_wall = 2
wall_width = 100
wall_height = 50

food = pygame.image.load('strawberry_new1.png')

pygame.init()
infoObj = pygame.display.Info()
display_width = infoObj.current_w
display_height = infoObj.current_h
screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('SimpleSnake')
clock = pygame.time.Clock()


class Move(enum.Enum):
    right = 0
    left = 1
    up = 2
    down = 3


class GameObject:
    def __init__(self):
        self.x = None
        self.y = None
        self.coord = self.generate_coord()

    def generate_coord(self):
        self.x = random.randint(min_coord, max_coord)
        self.y = random.randint(min_coord, max_coord)
        return self.x, self.y

    def get_coord(self):
        return self.coord


class Food(GameObject):
    def draw_food(self):
        screen.blit(food, self.coord)


class Wall(GameObject):
    def draw_wall(self):
        pygame.draw.rect(screen, yellow, [self.x, self.y, wall_width, wall_height])

