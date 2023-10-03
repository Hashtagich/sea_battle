from random import randint, choice
from time import sleep

from errors import *


class Dot:
    """Класс обозначающий точку на игровом поле. Принимает координаты, обозначение,
    признак того что по ней уже стреляли, и признак отображения её на поле или нет."""

    def __init__(self, x: int, y: int, shot: bool = False, mark: str = 'О', hid: bool = True):
        self.point = x, y
        self.shot = shot
        self.mark = mark
        self.hid = hid


class Ship:
    """Класс обозначающий корабль. Принимает длину корабля и начальную точку, вертикальное или
    горизонтальное расположение выбирается случайно. Анонимная функция self.live возвращает сумму всех
    не подстреленных точек данного корабля, что показывает здоровье корабля."""

    def __init__(self, length: int, dot_start: Dot):
        self.dot_start = dot_start
        self.length = length
        self.vertical = randint(0, 1)

        self.dots_list = None
        self.create_ship()
        self.live = lambda: sum([not j.shot for j in self.dots()])

    def create_ship(self) -> list:
        """Метод создаёт список на основании длинны, расположения и начальной точки корабля."""
        self.dots_list = []
        for i in range(self.length):
            dot = self.dot_start.point[not self.vertical] + i

            if self.vertical:
                self.dots_list.append(Dot(dot, self.dot_start.point[1]))
            else:
                self.dots_list.append(Dot(self.dot_start.point[0], dot))

        return self.dots_list

    def dots(self) -> list:
        """Метод возвращает список всех точек корабля."""
        return [i for i in self.dots_list]


class Board:
    """Класс обозначающий игровое поле(доску). Принимает название доски, отображается при выводе самой доски,
    и обозначение того показывать доску при выводе или нет."""

    def __init__(self, name_board: str = '', hid: bool = True):
        self.name_board = name_board
        self.miss = 'T'
        self.empty = 'О'
        self.hit = 'Х'
        self.mark_ship = '■'
        self.ship_list = []
        self.count_live_ship = 0
        self.hid = hid
        self.board = None
        self.create_empty_board()

    def create_empty_board(self) -> None:
        """Метод создаёт новую пустую игровую доску."""
        self.board = [[Dot(i, j, hid=self.hid) for i in range(LEN_MATRIX)] for j in range(LEN_MATRIX)]

    def add_ship(self, ship: Ship) -> None:
        """Метод добавляет корабль на игровую доску при условии что он не выходит за пределы полей и
        не пересекается с другими кораблями, иначе возбуждаются исключения BoardOutException или AddShipException.
        Self.hid применяется для того, чтобы дать точкам обозначение скрывать их при отображении или нет."""
        if ship.dot_start.point[not ship.vertical] + ship.length > LEN_MATRIX or \
                ship.dot_start.point[ship.vertical] > LEN_MATRIX:
            raise BoardOutException('Исключение BoardOutException, корабль за пределами поля.')

        if not any(map(lambda x: self.board[x.point[0]][x.point[1]].mark != self.empty, ship.dots())):
            for i in ship.dots():
                row, col = i.point
                if not self.hid:
                    i.hid = False
                self.board[row][col] = i
                self.board[row][col].mark = self.mark_ship
            self.contour(ship)

        else:
            raise AddShipException('Исключение AddShipException, клетка уже занята.')

    def contour(self, ship: Ship) -> None:
        """Метод обводит корабль по контуру, чтобы корректно разместить следующий корабль."""
        lst = (-1, 0, 1)

        for i in ship.dots():
            row, col = i.point

            for k in lst:
                for j in lst:
                    x, y = row + k, col + j

                    if LEN_MATRIX - 1 >= x >= 0 and LEN_MATRIX - 1 >= y >= 0:
                        if self.board[x][y].mark == self.empty:
                            self.board[x][y].mark = self.miss
                        else:
                            continue
                    else:
                        continue

    def shot(self, point: (tuple | list)) -> None:
        """Метод отвечает за выстрел по клетке. Проверяет свойство shot у заданной точки, если стреляли, то возбуждает
        исключение BoardOutException, в другом случаи меняется свойство(hid и shot) и вид отображения(mark) на доске."""
        x, y = point

        if self.board[x][y].shot:
            raise BoardOutException("Сюда уже стреляли. Повторный выстрел.")

        self.board[x][y].shot = True
        self.board[x][y].hid = False

        if self.board[x][y].mark == self.mark_ship:
            self.board[x][y].mark = self.hit

        else:
            self.board[x][y].mark = self.miss

    def show_board(self) -> None:
        """Метод выводит игровую доску на экран. horizontal_numbering - это ось нумерации столбцов.
        В данном методе применено выравнивание с помощью f-строк {:>2}.
        Доску можно сделать размерность до 99х99 не потеряв выравнивание."""
        print(self.name_board)

        horizontal_numbering = map(lambda num: f'{num + 1:>2} ', range(LEN_MATRIX))
        print(f'{"|":>4}{"|".join(horizontal_numbering)}|')

        for i in range(LEN_MATRIX):
            res = (f'{self.empty:^3}' if j.hid else f'{j.mark:^3}' for j in self.board[i])
            print(f'{i + 1:^3}|{"|".join(res)}|')
        print()


class Player:
    """Родительский класс Игрока. Принимает название доски и обозначение того показывать доску при
    выводе или нет что передать данные аргументы при создании доски.
    Метод ask необходимо прописать уже в каждом дочернем классе непосредственно."""

    def __init__(self, name_board: str = '', hid: bool = True):
        self.my_board = Board(hid=hid, name_board=name_board)

    def ask(self):
        """Метод для запроса координат, необходимо прописать в каждом дочернем классе."""
        pass

    def move(self, opponent_board) -> bool:
        """Метод отвечающий за ход игрока.
        Первоначально запускает метод ask для запроса координат, если будет возбуждено исключение то метод move
        начнётся заново. Если координаты корректные, то запускается метод shot по доске оппонента.
        В конце возвращается bool значение произошло попадание по кораблю или нет."""
        flag = False
        try:
            point = self.ask()
            if point is None:
                raise BoardOutException()

            if opponent_board.board[point[0]][point[1]].mark == opponent_board.mark_ship:
                flag = True

            opponent_board.shot(point)

        except (BoardOutException, InputException) as e:
            print(e)
            self.move(opponent_board)

        finally:
            return flag

    @staticmethod
    def correct_coordinates(point: (tuple | list)) -> bool:
        """Метод проверяет корректность ввода координат, возвращает bool значение."""
        return len(point) == 2 and all(map(str.isdigit, point)) and all(
            map(lambda x: int(x) in range(1, LEN_MATRIX + 1), point))


class User(Player):
    """Класс игрока-пользователя, дочерний класс класса Player с доработанным методом ask."""

    def ask(self) -> tuple:
        """Метод запрашивает у пользователя координаты, после ввода очищает консоль, и возбуждает исключение
        InputException в случаи некорректного ввода."""
        print("Ваш ход.")
        point = input(db_text['input_coordinates']).split()
        clear_console()

        if self.correct_coordinates(point):
            return tuple(int(x) - 1 for x in point)
        else:
            raise InputException("Не корректный ввод. Повторите ввод.")


class AI(Player):
    """Класс игрока-компьютера, дочерний класс класса Player с доработанным методом ask."""

    def __init__(self, name_board: str = '', hid: bool = True):
        super().__init__(name_board, hid)
        self.cache = set()

    def ask(self) -> tuple:
        """Метод осуществляется через бесконечный цикл.
        Случайным образом вводит координаты, проверяет, вводились они раньше или нет, если нет, то цикл прекращается."""
        print("Ход компьютера.")
        while True:

            point = (randint(0, LEN_MATRIX - 1), randint(0, LEN_MATRIX - 1))
            if point in self.cache:
                continue
            else:
                self.cache.add(point)
                break
        return point


class Game:
    """Класс отвечающий за игру "Морской бой"."""
    ANSWER_YES_TUPLE = ('yes', 'y', 'да', '+', 'конечно')
    ANSWER_NO_TUPLE = ('no', 'n', 'не', 'нет', '-', 'exit')

    def __init__(self):
        self.tuple_ships = (3, 2, 2, 1, 1, 1, 1)
        self.user = User(name_board='Ваше игровое поле', hid=False)
        self.ai = AI(name_board='Игровое поле противника', hid=True)
        self.user_board = self.user.my_board
        self.ai_board = self.ai.my_board

    def random_board(self, board) -> None:
        """Метод создаёт случайную игровую доску(размещает корабли), в случаи возбуждения исключения BoardOutException
         или AddShipException корабль не размещается и цикл продолжается. Если попытки count или self.tuple_ships
         закончатся, то цикл завершится. В случаи не размещения всех кораблей будет создана новая игровая доска,
         а неудавшаяся будет удалена. Также в методе присутствует cache чтобы повторно не прогонять через цикл уже
         применяемые координаты."""
        count = 100_000
        ind = 0
        cache = set()

        while ind != len(self.tuple_ships) and count > 0:
            try:
                count -= 1
                point = randint(0, LEN_MATRIX - 1), randint(0, LEN_MATRIX - 1)

                if point in cache:
                    continue
                else:
                    cache.add(point)
                    dot = Dot(*point, shot=False, mark='О', hid=not True)
                    ship = Ship(self.tuple_ships[ind], dot)
                    board.add_ship(ship)

            except (BoardOutException, AddShipException):
                pass

            else:
                board.ship_list.append(ship)
                ind += 1

        if len(board.ship_list) != len(self.tuple_ships):
            board.ship_list.clear()
            board.create_empty_board()
            self.random_board(board)

    @staticmethod
    def greet() -> None:
        """Метод выводит в консоль приветствие и краткую информацию по игре,
        между каждым сообщением задержка в несколько секунд."""
        for text in db_text['greet_list']:
            print(text)
            print()
            sleep(2)

    @staticmethod
    def end_game(board) -> bool:
        """Метод проверяет, закончились ли корабли (жизни) на переданной доске или нет и возвращает bool значение."""
        return bool(sum((i.live() for i in board.ship_list)))

    @staticmethod
    def next_move(player, board, opponent_board, text_win):
        """Метод для облегчения, написания алгоритма движка игры, в метод передаётся информация о том кто ходит.
        В зависимости от значения метода end_game и move будет выполнен данный метод или
        будет возбуждено исключение EndGameException или GoodShot."""
        move = player.move(opponent_board)
        if move and Game.end_game(board):
            if not Game.end_game(opponent_board):
                print(text_win)
                raise EndGameException

            print(f"{choice(db_text['shot'])} Повторный выстрел.")
            raise GoodShot
        else:
            print(f"{choice(db_text['miss'])} Переход хода.")

    def loop(self) -> None:
        """Метод представляет собой движок игры.
        1) Создаются две игровые доски пользователя и компьютера.
        2) Бесконечный цикл в котором поочерёдно ходят пользователь и компьютер, но если будет возбуждено исключение
        GoodShot или InputException передача хода не произойдёт, а будет совершен ещё один ход, а при исключении
        EndGameException цикл будет прерван (завершен) как и сам метод loop т.е. игра закончится.
        Ход осуществляется путём запуска метода next_move и передачей ему данных(словаря) о том кто ходит
        (пользователь или компьютер) из картежа players, ind тут является переключателем между пользователем
        и компьютером."""
        self.random_board(self.user_board)
        self.random_board(self.ai_board)

        ind = 0
        players = (
            {'player': self.user, 'board': self.user_board, 'opponent_board': self.ai_board,
             'text_win': db_text['win_user']},
            {'player': self.ai, 'board': self.ai_board, 'opponent_board': self.user_board,
             'text_win': db_text['win_ai']}
        )

        while True:
            self.user_board.show_board()
            self.ai_board.show_board()

            try:
                Game.next_move(**players[ind])

            except (GoodShot, InputException):
                continue

            except EndGameException:
                break

            else:
                ind = not ind

    def again(self) -> None:
        """Метод запускает новую игру в случаи положительного ответа."""
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

    def start(self) -> None:
        """Метод для запуска игры.
        1) Приветствие;
        2) Движок игры;
        3) Запуск новой игры или завершение программы."""
        self.greet()
        self.loop()
        self.again()


if __name__ == '__main__':
    game = Game()
    game.start()
