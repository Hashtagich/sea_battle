from random import randint

text_input_coordinates = '''Введите, через пробел, координаты для размещения корабля, например 1 2, цифры должны быть от 1 до 6 включительно!\n'''


class Dot:
    def __init__(self, x, y):
        self.point = x, y

    def __eq__(self, other):
        return self.point == other.point


class Ship:
    def __init__(self, length: int, dot_start, vertical=False):
        self.mark = '■'
        self.dot_start = dot_start
        self.length = length
        self.vertical = vertical
        self.live = length

    def dots(self):
        res = []
        # print(self.dot_start.point)
        for i in range(self.length):
            dot = self.dot_start.point[not self.vertical] + i

            if self.vertical:
                res.append(Dot(dot, self.dot_start.point[1]))
            else:
                res.append(Dot(self.dot_start.point[0], dot))

        return res

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


class Board:
    def __init__(self, hid=False):
        self.miss = 'T'  # '⏺'
        self.empty = 'О'
        self.hit = 'X'
        self.ship_list = []
        self.count_live_ship = 0
        self.hid = hid
        self.board = [[self.empty for _ in range(6)] for _ in range(6)]

    def add_ship(self, ship):
        try:
            if ship.dot_start.point[0] + ship.length > 6 or ship.dot_start.point[1] + ship.length > 6:
                raise IndexError
            else:
                for i in ship.dots():
                    row, col = i.point
                    print(row, col)
                    self.board[row][col] = ship.mark
                self.contour(ship)

        except IndexError:
            print("errooooooor")

    def contour(self, ship):
        for i in ship.dots():
            row, col = i.point

            if row not in (0, 5) and col not in (0, 5):

                for k in (-1, 1):
                    for j in (-1, 0, 1):

                        if self.board[row + k][col + j] == self.empty:
                            self.board[row + k][col + j] = self.miss
                        else:
                            continue


    def show_board(self, hid):
        print('  | 1 | 2 | 3 | 4 | 5 | 6 |')
        for i in range(6):
            print(f'{i + 1} | {" | ".join(self.board[i])} |')


dot = Dot(1, 1)
ship = Ship(3, dot, vertical=True)

board = Board()
board.add_ship(ship)
board.show_board(hid=board.hid)
