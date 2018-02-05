import random

PIECES = [
    [['*', '*', '*', '*'],
     [' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' ']],

    [[' ', '*', ' ', ' '],
     [' ', '*', ' ', ' '],
     [' ', '*', '*', ' '],
     [' ', ' ', ' ', ' ']],

    [[' ', ' ', '*', ' '],
     [' ', ' ', '*', ' '],
     [' ', '*', '*', ' '],
     [' ', ' ', ' ', ' ']],

    [[' ', ' ', '*', ' '],
     [' ', '*', '*', ' '],
     [' ', '*', ' ', ' '],
     [' ', ' ', ' ', ' ']],

    [[' ', '*', '*', ' '],
     [' ', '*', '*', ' '],
     [' ', ' ', ' ', ' '],
     [' ', ' ', ' ', ' ']],
]

moves = ['a', 'd', 'w', 's']


class Piece:
    shape = random.choice(PIECES)
    coordinates = [0, 0]  # track the upper left hand corner of the piece


class Board:
    board_state = None
    current_piece = None
    playing = None

    def __init__(self):
        self.playing = True
        self.board_state = [ [[' '] for _ in range(20)] for _ in range(20) ]
        for row in range(0, 19):
            self.board_state[row][0], self.board_state[row][19] = ['*'], ['*']
        self.board_state[19] = ['*'] * 20
        self.choose_new_piece()

    def display_current_board_state(self):
        for row in self.board_state:
            print(str(row).replace('[', '').replace(']', '').replace(',', '').replace("'", ''))

    # For this implementation, a location on the axis is randomly chosen. If a collision occurs, the game is over.
    # The game will not attempt to place a piece in an alternate spawning location
    def choose_new_piece(self):
        self.current_piece = Piece()
        self.current_piece.coordinates = [0, random.randint(1, 15)]

        try:
            for row in range(0, 4):
                for component in range(0, 4):
                    if self.current_piece.shape[row][component] == '*':
                        if self.board_state[row][component + self.current_piece.coordinates[1]] != ['*']:
                            self.board_state[row][component + self.current_piece.coordinates[1]] = ['*']
                        else:
                            self.playing = False
                            raise Exception('No more moves available! You lose!')
            if not self.check_for_legal_moves:
                self.playing = False
        except Exception as e:
            print(e)

    def get_move_from_user(self):
        move = input('(a) Shift Piece Left\n(d) Shift Piece Right\n'
                     '(w) Rotate Piece Counter Clockwise\n(s) Rotate Piece Clockwise\n')
        if move.lower() in moves:
            self.move_piece(move)
        else:
            print('That move type is undefined, try again!')
            self.get_move_from_user()

    def erase_old_shape(self, tentative_board_state, new_shape):
        for row in range(0,4):
            for component in range(0,4):
                if self.current_piece.shape[row][component] == '*' and new_shape[row][component] != '*':
                    tentative_board_state[row + self.current_piece.coordinates[0]][component + self.current_piece.coordinates[1]] = ' '
        return tentative_board_state

    def check_for_legal_moves(self):
        # check if we hit bottom first
        for row in range(3, -1, -1):
            if '*' in self.current_piece.shape[row]:
                if self.board_state[row + self.current_piece.coordinates[0] + 1][self.current_piece.shape[row].index('*')] == '*':
                    return False

        for move in moves:
            if self.attempt_move(move):
                return True
        return False

    # for some reason a shallow copy isn't being made, should really be debugged but time constrains are in place
    def copy_board_state(self):
        new_board = [ [[' '] for _ in range(20)] for _ in range(20) ]

        for row in range(0, 19):
            for component in range(0, 20):
                if self.board_state[row][component] == ['*']:
                    new_board[row][component] = ['*']
        new_board[19] = ['*'] * 20
        return new_board

    def attempt_move(self, move):
        tentative_board_state = self.copy_board_state()

        new_shape = self.current_piece.shape

        # a switch statement feels appropriate here but Python does not have switch statements
        if move == 'a':
            for row in range(3, -1, -1):
                for component in range(0, 4):
                    if self.current_piece.shape[row][component] == '*':
                        if tentative_board_state[row + self.current_piece.coordinates[0] + 1][component + self.current_piece.coordinates[1] - 1] != ['*']:
                            tentative_board_state[row + self.current_piece.coordinates[0] + 1][
                                component + self.current_piece.coordinates[1] - 1] = ['*']
                            tentative_board_state[row + self.current_piece.coordinates[0]][
                                component + self.current_piece.coordinates[1]] = [' ']
                        else:
                            return False
            tentative_coordinates = [self.current_piece.coordinates[0] + 1, self.current_piece.coordinates[1] - 1]

        elif move == 'd':
            for row in range(3, -1, -1):
                for component in range(3, -1, -1):
                    if self.current_piece.shape[row][component] == '*':
                        if tentative_board_state[row + self.current_piece.coordinates[0] + 1][component + self.current_piece.coordinates[1] + 1] != ['*']:
                            tentative_board_state[row + self.current_piece.coordinates[0] + 1][
                                component + self.current_piece.coordinates[1] + 1] = ['*']
                            tentative_board_state[row + self.current_piece.coordinates[0]][
                                component + self.current_piece.coordinates[1]] = [' ']
                        else:
                            return False
            tentative_coordinates = [self.current_piece.coordinates[0] + 1, self.current_piece.coordinates[1] + 1]

        elif move == 's':  # clockwise rotation
            new_shape = [[self.current_piece.shape[q][r] for q in range(3, -1, -1)] for r in range(0,4)]

            tentative_board_state = self.erase_old_shape(tentative_board_state, new_shape)

            for row in range(3, -1, -1):
                for component in range(0, 4):
                    if new_shape[row][component] == '*':
                        if tentative_board_state[row + self.current_piece.coordinates[0] + 1][component + self.current_piece.coordinates[1]] != ['*']:
                            tentative_board_state[row + self.current_piece.coordinates[0] + 1][
                                component + self.current_piece.coordinates[1]] = ['*']
                            tentative_board_state[row + self.current_piece.coordinates[0]][
                                component + self.current_piece.coordinates[1]] = [' ']
                        else:
                            return False

            tentative_coordinates = [self.current_piece.coordinates[0] + 1, self.current_piece.coordinates[1]]

        elif move == 'w':
            new_shape = [[self.current_piece.shape[q][r] for q in range(0,4)] for r in range(3, -1, -1)]

            tentative_board_state = self.erase_old_shape(tentative_board_state, new_shape)

            for row in range(3, -1, -1):
                for component in range(0, 4):
                    if new_shape[row][component] == '*':
                        if tentative_board_state[row + self.current_piece.coordinates[0] + 1][
                                    component + self.current_piece.coordinates[1]] != ['*']:
                            tentative_board_state[row + self.current_piece.coordinates[0] + 1][
                                component + self.current_piece.coordinates[1]] = ['*']
                            tentative_board_state[row + self.current_piece.coordinates[0]][
                                component + self.current_piece.coordinates[1]] = [' ']
                        else:
                            return False
            tentative_coordinates = [self.current_piece.coordinates[0] + 1, self.current_piece.coordinates[1]]
        else:
            return False

        # we got here so the move is valid and tentative board state is now the new board state
        return tentative_board_state, tentative_coordinates, new_shape

    def move_piece(self, move):
        try:
            new_board_state, new_coordinates, new_shape = self.attempt_move(move)
            self.board_state = new_board_state
            self.current_piece.coordinates = new_coordinates
            self.current_piece.shape = new_shape
            if not self.check_for_legal_moves():
                self.choose_new_piece()

        except Exception as e:
            print('That move is not legal, but there is a legal move available! Try again.')
            self.get_move_from_user()