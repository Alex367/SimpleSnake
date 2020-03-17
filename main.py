import sys
from snake_obj import Snake
from game_object import (black, green,
                         left_margin_field, top_margin_field,
                         field_width, field_height, Move,
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
            # compare food's and walls points
            x = Food()
            if len(self.list_wall) > 0:
                # when Wall is done and we need some foods
                food_p = x.get_coord()
                if self.compare_points(self.wall_points, food_p, 10, 20, 20) == 0:
                    del x
                    continue
            self.list_food.append(x)
            self.food_points.append(x.get_coord())
            i += 1

    def create_wall(self):
        i = 0
        while i < cnt_wall:
            w = Wall()
            self.list_wall.append(w)
            self.wall_points.append(w.get_coord())

            if len(self.list_wall) > 1:
                second_w = w.get_coord()
                first_w = self.wall_points[:-1]
                # compare wall and wall
                if self.compare_points(first_w, second_w, wall_width, 0, 5, tmp=True) == 0:
                    # print('deleted wall 1')
                    self.remove_wall()
                    del w
                    continue
                # compare wall and snake
                snake_coord = self.snake.get_snake_coord()
                i += 1
                new_second_w = self.wall_points[-1:]
                for z in snake_coord:
                    if self.compare_points(new_second_w, z, 20, 100, 100) == 0:
                        # print('deleted wall 2')
                        self.remove_wall()
                        i -= 1
                        del w
                        break
            # compare wall and snake
            else:
                snake_coord = self.snake.get_snake_coord()
                i += 1
                for p in snake_coord:
                    if self.compare_points(self.wall_points, p, 20, 100, 100) == 0:
                        # print('deleted wall 3')
                        self.remove_wall()
                        i -= 1
                        del w
                        break

    @staticmethod
    def compare_points(w_points, f_points, center_margin_x, l_margin, r_margin, tmp=None):
        center_margin_y = center_margin_x
        if tmp:
            center_margin_y = wall_height
        for j in w_points:
            if (j[0] - l_margin < f_points[0] < j[0] + wall_width + r_margin or
                j[0] - l_margin < f_points[0] + center_margin_x < j[0] + wall_width + r_margin) and\
                    (j[1] - l_margin < f_points[1] < j[1] + wall_height + r_margin or
                     j[1] - l_margin < f_points[1] + center_margin_y < j[1] + wall_height + r_margin):
                return 0
        return 1

    def remove_wall(self):
        self.list_wall.pop()
        self.wall_points.pop()

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
