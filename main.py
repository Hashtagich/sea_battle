from random import randint

text_input_coordinates = '''Введите, через пробел, координаты для размещения корабля, например 1 2, цифры должны быть от 1 до 6 включительно!\n'''


class GameBoard:
    def __init__(self, hit=False):
        self.miss = 'T'
        self.empty = 'О'
        self.hit = 'X'
        self.ship_list = []
        self.count_ship = 0
        self.hit = hit
        self.board = [[self.empty for _ in range(6)] for _ in range(6)]

    def shop_board(self):
        print('  | 1 | 2 | 3 | 4 | 5 | 6 |')
        for i in range(6):
            print(f'{i + 1} | {" | ".join(self.board[i])} |')


class Dot:
    def __init__(self, x, y):
        self.point = x, y

    def __eq__(self, other):
        return self.point == other


class Ship:
    def __init__(self, length: int, d, vertical=False):
        self.mark = '■'
        self.length = length
        self.vertical = vertical
        self.dot = d

    # @staticmethod
    # def correct_coordinates(point):
    #     return len(point) == 2 and all(map(str.isdigit, point)) and all(map(lambda x: int(x) in range(1, 7), point))
    #
    # def post_ship(self, coordinates: str):
    #     point = coordinates.split()
    #
    #     if self.correct_coordinates(point):
    #         return point
    #     else:
    #         print('Некорректный ввод!')
    #         self.post_ship(input(text_input_coordinates))
    #
    # def create_ship(self):
    #     return [self.mark] * self.length
