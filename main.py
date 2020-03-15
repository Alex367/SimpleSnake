import sys
from snake_obj import Snake
from game_object import (black, green,
                         left_margin_field, top_margin_field,
                         field_width, field_height, Move, itertools,
                         pygame, screen, Food, Wall, cnt_food, cnt_wall,
                         wall_width, wall_height)


class Field:
    def __init__(self, color, *field_size, border):
        self.field_color = color
        self.field_size = field_size
        self.field_border = border
        self.score = 0
        # create wall
        self.list_wall = []
        self.wall_points = []
        # create food
        self.list_food = []
        self.food_points = []
        self.create_food()
        # create snake
        self.snake = Snake()

    def draw_field(self, change_sn_move):
        # draw field
        pygame.draw.rect(screen, self.field_color, self.field_size, self.field_border)
        # wall
        if self.score > 2:
            if len(self.list_wall) == 0:
                self.create_wall()
            for i in self.list_wall:
                i.draw_wall()
        # draw food, check food's object existence
        if len(self.list_food) == 0:
            self.create_food()
        for i in self.list_food:
            i.draw_food()
        # draw snake
        if change_sn_move is not None:
            # change_sn_move
            self.snake.draw_snake(self.wall_points, move=change_sn_move)
        else:
            self.snake.draw_snake(self.wall_points)
        # which food was eaten
        eaten = self.snake.lunch_snake(self.food_points)

        if eaten is not None:
            for i in self.list_food:
                if self.list_food.index(i) == eaten:
                    del self.list_food[eaten]
                    del self.food_points[eaten]
                    self.score += 1
                    break
        # score
        self.draw_score()

    def create_food(self):
        i = 0
        while i < cnt_food:
            x = Food()
            if len(self.wall_points) > 0:
                # when Wall is done and we need some foods
                if self.compare_food_wall(x):
                    self.list_food.append(x)
                    # write coordinate of food
                    self.food_points.append(x.get_coord())
                    i += 1
                else:
                    del x
            else:
                self.list_food.append(x)
                self.food_points.append(x.get_coord())
                i += 1

    def create_wall(self):
        i = 0
        while i < cnt_wall:
            w = Wall()
            self.list_wall.append(w)
            if len(self.list_wall) > 1:
                if self.compare_walls_coord() == 0:
                    # print('del')
                    self.list_wall.pop()
                    del w
                    continue
            if self.compare_wall_snake(i) == 0:
                self.list_wall.pop()
                del w
                continue
            self.wall_points.append(w.get_coord())
            i += 1
        print(self.wall_points)

    def compare_wall_snake(self, index_wall):
        snake_coord = self.snake.get_snake_coord()
        for i, j in enumerate(self.list_wall):
            if i == index_wall:
                for z in snake_coord:
                    if (j.x - 100 < z[0] < j.x + wall_width + 50 or
                        j.x - 100 < z[0] + 20 < j.x + wall_width + 50) and\
                            (j.y - 100 < z[1] < j.y + wall_height + 50 or
                             j.y - 100 < z[1] + 20 < j.y + wall_height + 50):
                        # print('del')
                        return 0
        return 1

    def compare_walls_coord(self):
        for i, j in itertools.combinations(self.list_wall, 2):
            # print('first ', i.x, i.y)
            # print('sec ', j.x, j.y)
            if (i.x < j.x < i.x + wall_width + 5 or
                i.x < j.x + wall_width < i.x + wall_width + 5) and\
                    (i.y < j.y < i.y + wall_height + 5 or
                     i.y < j.y + wall_height < i.y + wall_height + 5):
                # print('wa')
                return 0
        return 1

    def compare_food_wall(self, f_points):
        for j in self.wall_points:
            if (j[0] - 20 < f_points.x < j[0] + wall_width + 20 or
                j[0] - 20 < f_points.x + 10 < j[0] + wall_width + 20) and\
                    (j[1] - 20 < f_points.y < j[1] + wall_height + 20 or
                     j[1] - 20 < f_points.y + 10 < j[1] + wall_height + 20):
                return 0
        return 1

    def draw_score(self):
        font = pygame.font.Font('freesansbold.ttf', 18)
        text = font.render("Score: " + str(self.score), True, green)
        screen.blit(text, (300, 10))
        pygame.display.update()


def start_game():
    create_field = Field(green, left_margin_field, top_margin_field, field_width, field_height, border=1)
    move_snake = None
    prev_move = Move.right.name

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and prev_move != Move.up.name:
                    move_snake = prev_move = Move.down.name
                elif event.key == pygame.K_UP and prev_move != Move.down.name:
                    move_snake = prev_move = Move.up.name
                elif event.key == pygame.K_RIGHT and prev_move != Move.left.name:
                    move_snake = prev_move = Move.right.name
                elif event.key == pygame.K_LEFT and prev_move != Move.right.name:
                    move_snake = prev_move = Move.left.name

        screen.fill(black)
        create_field.draw_field(move_snake)
        move_snake = None
        pygame.display.update()


if __name__ == '__main__':
    start_game()
