from random import randint

text_coordinates = '''Введите, через пробел, координаты для размещения корабля. 
Например 1 2, цифры должны быть от 1 до 6 включительно!
Первая строка, вторая столбец.\n'''


class Dot:
    def __init__(self, x: int, y: int, shot: bool = False, mark: str = 'О', hid: bool = True):
        self.point = x, y
        self.shot = shot
        self.mark = mark
        self.hid = hid

    def __eq__(self, other):
        return self.point == other.point


class Ship:
    def __init__(self, length: int, dot_start, vertical: bool = False):
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


class Board:
    LEN_MATRIX = 6

    def __init__(self, hid: bool = True):
        self.miss = 'T'  # '⏺'
        self.empty = 'О'
        self.hit = 'X'
        self.mark_ship = '■'
        self.ship_list = []
        self.count_live_ship = 0
        self.hid = hid
        self.board = [[Dot(i, j) for i in range(Board.LEN_MATRIX)] for j in range(Board.LEN_MATRIX)]

    def add_ship(self, ship):
        try:
            if ship.dot_start.point[0] + ship.length > 6 or ship.dot_start.point[1] + ship.length > 6:
                raise IndexError
            else:
                for i in ship.dots():
                    row, col = i.point
                    # print(row, col)
                    self.board[row][col].mark = self.mark_ship
                self.contour(ship)

        except IndexError:
            print("error def add_ship")

    def contour(self, ship):
        for i in ship.dots():
            row, col = i.point

            if row not in (0, 5) and col not in (0, 5):

                for k in (-1, 1):
                    for j in (-1, 0, 1):

                        if self.board[row + k][col + j].mark == self.empty:
                            self.board[row + k][col + j].mark = self.miss

                        else:
                            continue

    @staticmethod
    def out(point):
        x, y = point
        return x > Board.LEN_MATRIX or y > Board.LEN_MATRIX

    def shot(self, point):
        x, y = point
        try:
            if Board.out(point):
                raise IndexError
            else:

                try:
                    if self.board[x][y].shot:
                        raise Exception
                    else:
                        self.board[x][y].shot = True
                        self.board[x][y].hid = False
                        self.board[x][y].mark = self.miss

                except Exception as e:
                    print(e, 'error2!!!!')

        except IndexError as e:
            print(e, 'error1!!!!')

    def show_board(self):
        if self.hid:
            print('  | 1 | 2 | 3 | 4 | 5 | 6 |')
            for i in range(Board.LEN_MATRIX):
                res = (self.empty if j.hid else j.mark for j in self.board[i])
                print(f'{i + 1} | {" | ".join(res)} |')


class Player:
    def __init__(self, hid: bool = True):
        self.my_board = Board(hid=hid)
        self.opponent_board = Board(hid=hid)

    def ask(self):
        pass

    def move(self, opponent_board):
        point = self.ask()
        print('Стреляю!', point)  # проверочная
        opponent_board.shot(point)

    @staticmethod
    def correct_coordinates(point):
        return len(point) == 2 and all(map(str.isdigit, point)) and all(
            map(lambda x: int(x) in range(1, Board.LEN_MATRIX + 1), point))


class User(Player):
    def ask(self):
        print("Ваш ход.")
        point = input(text_coordinates).split()

        if self.correct_coordinates(point):
            return tuple(int(x) - 1 for x in point)
        else:
            print('Некорректный ввод координат!')
            self.ask()


class AI(Player):
    def ask(self):
        print("Ход компьютера.")
        return randint(0, 5), randint(0, 5)


class Game:
    def __init__(self):
        self.user = User()
        self.ai = AI()
        self.user_board = self.user.my_board
        self.ai_board = self.ai.my_board

    def random_board(self):
        pass

    @staticmethod
    def greet():
        print('Добро пожаловать в игру "Морской бой!"\n')

    def loop(self):
        while True:
            self.user.move(self.ai_board)

    def start(self):
        self.greet()
        self.loop()


if __name__ == '__main__':
    game = Game()
    game.start()
