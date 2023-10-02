import os
from random import randint
from time import sleep

# text_coordinates = '''Введите, через пробел, координаты для размещения корабля.
# Например, 1 2, цифры должны быть от 1 до 6 включительно!
# Первая строка, вторая столбец.\n'''

db_text = {
    'input_coordinates': 'ввод\n',
    'win_ai': 'Все Ваши корабли уничтожены!\nВы проиграли.  ¯\_(ツ)_/¯ \n',
    'win_user': 'Все корабли противника уничтожены!\nВы победили!\n',
    'shot': ('Попадание!', 'Прямо в цель!', "Есть пробитие!"),
    'miss': ('Мимо.', 'Промашка.', "Почти попал."),
}


def clear_console() -> None:
    """Функция для очистки консоли от лишнего текста для улучшения визуализации игры."""
    os.system('cls' if os.name == 'nt' else 'clear')


class BoardOutException(Exception):
    pass


class InputException(Exception):
    pass


class EndGameException(Exception):
    pass


class GoodShot(Exception):
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


class Ship:
    def __init__(self, length: int, dot_start: Dot):
        self.dot_start = dot_start
        self.length = length
        self.vertical = randint(0, 1)

        self.dots_list = None
        self.create_ship()
        self.live = lambda: sum([not j.shot for j in self.dots()])

    def create_ship(self):
        self.dots_list = []
        for i in range(self.length):
            dot = self.dot_start.point[not self.vertical] + i

            if self.vertical:
                self.dots_list.append(Dot(dot, self.dot_start.point[1]))
            else:
                self.dots_list.append(Dot(self.dot_start.point[0], dot))

        return self.dots_list

    def dots(self):
        return [i for i in self.dots_list]


class Board:
    LEN_MATRIX = 6

    def __init__(self, name_board: str = '', hid: bool = True):
        self.name_board = name_board
        self.miss = 'T'  # '⏺'
        self.empty = 'О'
        self.hit = 'X'
        self.mark_ship = '■'
        self.ship_list = []
        self.count_live_ship = 0
        self.hid = hid
        self.board = None
        self.create_empty_board()

    def create_empty_board(self):
        self.board = [[Dot(i, j) for i in range(Board.LEN_MATRIX)] for j in range(Board.LEN_MATRIX)]

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
                self.board[row][col] = i
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

    # @staticmethod
    # def out(point):
    #     x, y = point
    #     return x > Board.LEN_MATRIX or y > Board.LEN_MATRIX

    def shot(self, point):
        x, y = point
        #
        # if Board.out(point):
        #     print('работает!')
        #     raise EndGameException("ошибка №1, введённые координаты за пределами доски")

        if self.board[x][y].shot:
            raise BoardOutException("Сюда уже стреляли. Повторный выстрел.")

        self.board[x][y].shot = True
        self.board[x][y].hid = False

        if self.board[x][y].mark == self.mark_ship:
            self.board[x][y].mark = self.hit

        else:
            self.board[x][y].mark = self.miss

    def show_board(self):
        if self.hid:
            print(self.name_board)
            print('  | 1 | 2 | 3 | 4 | 5 | 6 |')
            for i in range(Board.LEN_MATRIX):
                res = (self.empty if j.hid else j.mark for j in self.board[i])
                print(f'{i + 1} | {" | ".join(res)} |')
            print()


class Player:
    def __init__(self, name_board: str = '', hid: bool = True):
        self.my_board = Board(hid=hid, name_board=name_board)

    def ask(self):
        pass

    def move(self, opponent_board):
        flag = False
        try:
            point = self.ask()
            if point is None:
                raise BoardOutException("ошибка №3")

            if opponent_board.board[point[0]][point[1]].mark == opponent_board.mark_ship:
                flag = True

            opponent_board.shot(point)
        # except InputException as e:
        #     print(e)
        #     self.move(opponent_board)

        except (EndGameException, BoardOutException, InputException) as e:
            print(e)
            self.move(opponent_board)

        finally:
            return flag

    @staticmethod
    def correct_coordinates(point):

        return len(point) == 2 and all(map(str.isdigit, point)) and all(
            map(lambda x: int(x) in range(1, Board.LEN_MATRIX + 1), point))


class User(Player):
    def ask(self):
        print("Ваш ход.")
        point = input(db_text['input_coordinates']).split()

        if self.correct_coordinates(point):
            return tuple(int(x) - 1 for x in point)
        else:
            raise InputException("Не корректный ввод. Повторите ввод.")


class AI(Player):
    def __init__(self, name_board: str = '', hid: bool = True):
        super().__init__(name_board, hid)
        self.cache = set()

    def ask(self):
        print("Ход компьютера.")
        while True:

            point = (randint(0, 5), randint(0, 5))
            if point in self.cache:
                continue
            else:
                self.cache.add(point)
                break
        return point


class Game:
    ANSWER_YES_TUPLE = ('yes', 'y', 'да', '+', 'конечно')
    ANSWER_NO_TUPLE = ('no', 'n', 'не', 'нет', '-', 'exit')

    def __init__(self):
        self.tuple_ships = (3, 2, 2, 1, 1, 1, 1)
        self.user = User(name_board='Ваше игровое поле')
        self.ai = AI(name_board='Игровое поле противника')
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

            except (BoardOutException, AddShipException):  # as e:
                # print(e)
                pass

            else:
                board.ship_list.append(ship)
                ind += 1

        if len(board.ship_list) != len(self.tuple_ships):
            board.ship_list.clear()
            board.create_empty_board()
            self.random_board(board)

    @staticmethod
    def greet():
        print('Добро пожаловать в игру "Морской бой!"\n')

    @staticmethod
    def end_game(board):
        return bool(sum((i.live() for i in board.ship_list)))

    @staticmethod
    def next_move(player, board, opponent_board, text_win):
        move = player.move(opponent_board)
        if move and Game.end_game(board):
            if not Game.end_game(opponent_board):
                print(text_win)
                raise BoardOutException

            print(f"{db_text['shot'][randint(1, 2)]} Повторный выстрел.")
            raise GoodShot
        else:
            print(f"{db_text['miss'][randint(1, 2)]} Переход хода.")

    def loop(self):
        self.random_board(self.user_board)
        self.random_board(self.ai_board)

        ind = 0
        flag = (
            {'player': self.user, 'board': self.user_board, 'opponent_board': self.ai_board,
             'text_win': db_text['win_user']},
            {'player': self.ai, 'board': self.ai_board, 'opponent_board': self.user_board,
             'text_win': db_text['win_ai']}
        )

        while True:
            self.user_board.show_board()
            self.ai_board.show_board()

            try:
                Game.next_move(**flag[ind])

            except (GoodShot, InputException):
                continue

            except BoardOutException:
                break

            else:
                ind = not ind

    def again(self):
        flag = True

        while flag:
            answer = input('Желаете сыграть ещё одну игру? Y\\N\n').lower()

            if answer in Game.ANSWER_YES_TUPLE:
                flag = False

                self.__init__()
                self.start()
            elif answer in Game.ANSWER_NO_TUPLE:
                flag = False

                print('Всего хорошего!')
                sleep(1)
            else:
                print('Некорректный ввод. Повторите ввод.')
                continue

    def start(self):
        self.greet()
        self.loop()
        self.again()


if __name__ == '__main__':
    game = Game()
    game.start()
