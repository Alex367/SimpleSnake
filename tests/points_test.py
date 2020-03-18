import unittest
from game_object import compare_points, wall_width


class TestComparePoints(unittest.TestCase):
    def setUp(self):
        self.f_wall = [[200, 200]]
        self.res = None

    # walls
    def test_walls_negative(self):
        # max point x
        s_wall = [304, 200]
        self.res = compare_points(self.f_wall, s_wall, wall_width, 0, 5, True)
        self.assertEqual(self.res, 0)

    def test_walls_positive(self):
        s_wall = [400, 200]
        self.res = compare_points(self.f_wall, s_wall, wall_width, 0, 5, True)
        self.assertEqual(self.res, 1)

    # food
    def test_food_negative(self):
        food_points = [230, 220]
        self.res = compare_points(self.f_wall, food_points, 10, 20, 20)
        self.assertTrue(self.res == 0)

    def test_food_positive(self):
        food_points = [400, 200]
        self.res = compare_points(self.f_wall, food_points, 10, 20, 20)
        self.assertTrue(self.res == 1)

    def tearDown(self):
        print('Result in test :', self.res)


if __name__ == '__main__':
    unittest.main()
