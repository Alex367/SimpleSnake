import sys
import pygame
import random
import enum

# field
size = width, height = 600, 600
black = 0, 0, 0
green = 0, 255, 0
red = 225, 0, 0
purple = 218, 112, 214
# yellow = 240, 230, 140
field_width = field_height = 500
left_margin_field = top_margin_field = 50
# food
cnt_food = 3
food = pygame.image.load('strawberry_new1.png')
# coordinate
max_x = 100
max_y = 450
# snake
width_snake = height_snake = 20

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('SimpleSnake')
clock = pygame.time.Clock()


class Move(enum.Enum):
    right = 0
    left = 1
    up = 2
    down = 3


class Snake:
    def __init__(self):
        self.snake_body = [[100, 80], ]
        self.snake_way = Move.right.name

    def draw_snake(self, move=None, was_change=False):
        if move is not None:
            self.snake_way = move
        if was_change is False:
            # create a new head and remove an old tail
            head = self.snake_body[-1]
            self.snake_body.pop(0)

            self.change_head(head)

        for i in self.snake_body:
            # paint snake
            head = self.snake_body[-1]
            if i[0] == head[0] and i[1] == head[1]:
                pygame.draw.rect(screen, red, [i[0], i[1], width_snake, height_snake])
            else:
                pygame.draw.rect(screen, purple, [i[0], i[1], width_snake, height_snake])

        clock.tick(20)
        pygame.display.update()
        self.check_crash()

    def check_crash(self):
        head = self.snake_body[-1]
        # border crash
        for i in range(21):
            if head[0] + i > field_width + left_margin_field-10 or head[0] + i <= 50 or \
                    head[1] + i > field_height + top_margin_field-10 or head[1] + i <= 50:
                sys.exit()

        # snake itself crash
        if len(self.snake_body) > 3:
            body = self.snake_body[:-3]
            for i in body:
                for j in range(21):
                    if i[0] < head[0] + j < i[0] + 10 and i[1] < head[1] + j < i[1] + 10:
                        sys.exit()

    def lunch_time_snake(self, food_points):
        snake_head = self.snake_body[-1]
        for i in food_points:
            for j in range(21):
                for p in range(21):
                    if i[0] <= snake_head[0] + j <= i[0]+10 and i[1] <= snake_head[1] + p <= i[1]+10:
                        self.change_head(snake_head)
                        self.draw_snake(was_change=True)
                        return food_points.index(i)

    def change_head(self, snake_head):
        if self.snake_way == Move.right.name:
            self.snake_body.append([snake_head[0] + 10, snake_head[1]])
        elif self.snake_way == Move.left.name:
            self.snake_body.append([snake_head[0] - 10, snake_head[1]])
        elif self.snake_way == Move.down.name:
            self.snake_body.append([snake_head[0], snake_head[1] + 10])
        else:
            self.snake_body.append([snake_head[0], snake_head[1] - 10])


class Field:
    def __init__(self, color, *field_size, border):
        self.field_color = color
        self.field_size = field_size
        self.field_border = border
        self.list_food = []
        self.food_points = []
        # create food
        self.create_food()
        # create snake
        self.snake = Snake()
        self.score = 0

    def draw_field(self, change_sn_move):
        # draw field
        pygame.draw.rect(screen, self.field_color, self.field_size, self.field_border)
        # draw food, check food's object existence
        if self.list_food:
            for i in self.list_food:
                i.draw_food()
        else:
            # create a new food again
            self.create_food()
        # draw snake
        if change_sn_move is not None:
            # change_sn_move
            self.snake.draw_snake(move=change_sn_move)
        else:
            self.snake.draw_snake()
        # which food was eaten
        eaten = self.snake.lunch_time_snake(self.food_points)

        if eaten is not None:
            for i in self.list_food:
                if self.list_food.index(i) == eaten:
                    del self.list_food[eaten]
                    del self.food_points[eaten]
                    self.score += 1
                    break
        # print score
        self.draw_score()

    def create_food(self):
        for i in range(cnt_food):
            x = Food()
            self.list_food.append(x)
            # write coordinate of food
            self.food_points.append(x.get_food_coord())

    def draw_score(self):
        font = pygame.font.Font('freesansbold.ttf', 18)
        text = font.render("Score: " + str(self.score), True, green)
        screen.blit(text, (300, 10))
        pygame.display.update()


class Food:
    def __init__(self):
        self.x = None
        self.y = None
        self.coord = self.generate_coord()

    def draw_food(self):
        screen.blit(food, self.coord)

    def get_food_coord(self):
        return self.coord

    def generate_coord(self):
        self.x = random.randint(max_x, max_y)
        self.y = random.randint(max_x, max_y)
        return self.x, self.y


def start_game():
    create_field = Field(green, left_margin_field, top_margin_field, field_width, field_height, border=1)
    move_snake = None
    prev_move = Move.right.name

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if prev_move == Move.up.name:
                        break
                    else:
                        move_snake = prev_move = Move.down.name
                elif event.key == pygame.K_UP:
                    if prev_move == Move.down.name:
                        break
                    else:
                        move_snake = prev_move = Move.up.name
                elif event.key == pygame.K_RIGHT:
                    if prev_move == Move.left.name:
                        break
                    else:
                        move_snake = prev_move = Move.right.name
                elif event.key == pygame.K_LEFT:
                    if prev_move == Move.right.name:
                        break
                    else:
                        move_snake = prev_move = Move.left.name

        screen.fill(black)
        create_field.draw_field(move_snake)
        move_snake = None
        pygame.display.update()


if __name__ == '__main__':
    start_game()
