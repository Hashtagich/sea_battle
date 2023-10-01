from random import randint


class BoardOutException(Exception):
    pass


class AddShipException(Exception):
    pass


class BoardCreateException(Exception):
    pass


class Dot:
    def __init__(self, x: int, y: int, shot: bool = False, mark: str = 'О', hid: bool = not True):
        self.point = x, y
        self.shot = shot
        self.mark = mark
        self.hid = hid

    def __eq__(self, other):
        return self.point == other.point


class Ship:
    def __init__(self, length: int, dot_start: Dot):
        self.dot_start = dot_start
        self.length = length
        self.vertical = randint(0, 1)
        self.live = length

    def dots(self):
        res = []
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
        self.board = None
        # self.board = [[Dot(i, j) for i in range(Board.LEN_MATRIX)] for j in range(Board.LEN_MATRIX)]
        self.create_empty_board()

    def create_empty_board(self):
        self.board = [[Dot(i, j) for i in range(Board.LEN_MATRIX)] for j in range(Board.LEN_MATRIX)]

    @staticmethod
    def out(point):
        print('Запуск out')
        x, y = point
        return x > Board.LEN_MATRIX or y > Board.LEN_MATRIX

    def add_ship(self, ship):
        if ship.dot_start.point[not ship.vertical] + ship.length > Board.LEN_MATRIX or \
                ship.dot_start.point[ship.vertical] > Board.LEN_MATRIX:
            raise BoardOutException('Исключение BoardOutException, корабль за пределами поля.')

            # На случай если верхние 2 строки не будут работать корректно
            # if ship.vertical:
            #     if ship.dot_start.point[0] + ship.length > Board.LEN_MATRIX or \
            #             ship.dot_start.point[1] > Board.LEN_MATRIX:
            #         raise BoardOutException('Исключение BoardOutException, корабль за пределами поля.')
            #
            # else:
            #     if ship.dot_start.point[1] + ship.length > Board.LEN_MATRIX or \
            #             ship.dot_start.point[0] > Board.LEN_MATRIX:
            #         raise BoardOutException('Исключение BoardOutException, корабль за пределами поля.')

        if not any(map(lambda x: self.board[x.point[0]][x.point[1]].mark != self.empty, ship.dots())):
            # if all(map(lambda x: self.board[x.point[0]][x.point[1]].mark == self.empty, ship.dots())):
            for i in ship.dots():
                row, col = i.point
                self.board[row][col].mark = self.mark_ship
            self.contour(ship)

        else:
            raise AddShipException('Исключение AddShipException, клетка уже занята.')

    def contour(self, ship):
        lst = (-1, 0, 1)

        for i in ship.dots():
            row, col = i.point

            for k in lst:
                for j in lst:
                    x, y = row + k, col + j

                    if 5 >= x >= 0 and 5 >= y >= 0:
                        if self.board[x][y].mark == self.empty:
                            self.board[x][y].mark = self.miss
                        else:
                            continue
                    else:
                        continue

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


class Game:
    def __init__(self):
        self.tuple_ships = (3, 2, 2, 1, 1, 1, 1)

        self.user = Player()
        self.ai = Player()
        self.user_board = self.user.my_board
        self.ai_board = self.ai.my_board

    def random_board(self, board):
        count = 100_000
        ind = 0
        cache = set()

        while ind != len(self.tuple_ships) and count > 0:
            try:
                count -= 1
                point = randint(0, 5), randint(0, 5)

                if point in cache:
                    continue
                else:
                    cache.add(point)
                    dot = Dot(*point, shot=False, mark='О', hid=not True)
                    ship = Ship(self.tuple_ships[ind], dot)
                    board.add_ship(ship)

            except (BoardOutException, AddShipException) as e:
                print(e, count, '!!!!!!!!')

            else:
                # проверочный блок
                print(f'Корабль №{ind + 1} поставлен на нач координат {point[0] + 1, point[1] + 1}, попытка №{count}\n')
                board.show_board()
                #########
                board.ship_list.append(ship)
                ind += 1
        print('создание кончилось!')
        if len(board.ship_list) != len(self.tuple_ships):
            board.ship_list.clear()
            board.create_empty_board()
            self.random_board(board)
        else:
            print('удалось')


g = Game()
g.random_board(g.user_board)
g.user_board.show_board()

g.random_board(g.ai_board)
g.ai_board.show_board()

# ship_1 = Ship(3, Dot(1, 1))
# ship_2 = Ship(2, Dot(2, 4))
# boar = Board()
# boar.add_ship(ship_1)
# boar.add_ship(ship_2)
# boar.show_board()
