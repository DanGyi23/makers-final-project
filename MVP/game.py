import chessboard
import turn
import player
from king import King
from piece import Piece
from checkmate import Checkmate
from draw import Draw


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

    def is_checkmate(self):
        if Checkmate(self).is_checkmate():
            return True
        else:
            return False

    def is_draw(self):
        if Draw(self).is_draw():
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
