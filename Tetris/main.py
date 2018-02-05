
from Models import Board


print('WELCOME TO TETRIS!')
game_board = Board()
while game_board.playing:
    game_board.display_current_board_state()
    game_board.get_move_from_user()