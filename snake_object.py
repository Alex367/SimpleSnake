import sys
from game_object import (Move, pygame, screen, red, purple, clock,
                         field_width, left_margin_field,
                         field_height, top_margin_field, compare_points)

width_snake = height_snake = 20


class Snake:
    def __init__(self):
        self.snake_body = [[100, 80], ]
        self.snake_way = Move.right.name

    def draw_snake(self, wall_points=None, move=None, was_change=False):
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
        self.check_crash(wall_points)

    def check_crash(self, wall_points):
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

        # wall crash
        if wall_points is not None:
            if compare_points(wall_points, head, 20, 0, 0) == 0:
                sys.exit()

    def lunch_snake(self, food_points):
        snake_head = self.snake_body[-1]
        for i in food_points:
            if (snake_head[0] < i[0] < snake_head[0] + 20 or
                snake_head[0] < i[0] + 10 < snake_head[0] + 20) and\
                    (snake_head[1] < i[1] < snake_head[1] + 20 or
                     snake_head[1] < i[1] + 10 < snake_head[1] + 20):
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

    def get_snake_coord(self):
        return self.snake_body
