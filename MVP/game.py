import chessboard
import turn
import player
from king import King
from piece import Piece
from checkmate import Checkmate


class Game:

    def __init__(self, p1_name, p2_name):
        self.board = chessboard.ChessBoard()
        self.player_1 = player.Player(p1_name, "White")
        self.player_2 = player.Player(p2_name, "Black")
        self.p1_turn = True
        self.log = []

    def execute_turn(self, turn_from_x, turn_from_y, turn_to_x, turn_to_y):
        try:
            self.check_player_owns_piece(int(turn_from_x), int(turn_from_y))
            turn.Turn(self.board, self.player_1, self.player_2).move(int(turn_from_x), int(turn_from_y), int(turn_to_x), int(turn_to_y))
            self.log_turn(int(turn_from_x), int(turn_from_y), int(turn_to_x), int(turn_to_y))
            self.p1_turn = not self.p1_turn
            return 'valid move'
        except:
            return 'invalid move'

    def revert_turn(self, turn_from_x, turn_from_y, turn_to_x, turn_to_y, original_object, target_object):
            self.board.board[turn_from_x][turn_from_y] = original_object
            self.board.board[turn_to_x][turn_to_y] = target_object
            self.p1_turn = not self.p1_turn

    def get_original_pieces(self, turn_from_x, turn_from_y, turn_to_x, turn_to_y):
            original_square = self.board.board[turn_from_x][turn_from_y]
            moved_to = self.board.board[turn_to_x][turn_to_y]
            return [original_square, moved_to]

    def is_checkmate(self):
        if Checkmate(self).is_checkmate():
            return True
        else:
            return False

    def log_turn(self, turn_from_x, turn_from_y, turn_to_x, turn_to_y):
        colour = 'White' if self.p1_turn else 'Black'
        self.log.append([colour, turn_from_x, turn_from_y, turn_to_x, turn_to_y])

    def check_player_owns_piece(self, x, y):
        colour = 'White' if self.p1_turn else 'Black'
        if self.board.board[x][y].colour != colour:
            raise ValueError("PlayerDoesNotOwnPiece")

