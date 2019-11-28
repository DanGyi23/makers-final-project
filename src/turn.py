import bishop
import copy
import king
import knight
import pawn
import piece
import queen
import rook

class Turn:
    def __init__(self, ruleset, board, log, player_1, player_2):
        self.ruleset = ruleset
        self.board = board
        self.game_log = log
        self.player_1 = player_1
        self.player_2 = player_2

    def move(self, start_row, start_col, end_row, end_col):
        piece_to_move = self.board[start_row][start_col]
        if self.ruleset.check_for_invalid_move(self.board, start_row, start_col, end_row, end_col):
            raise ValueError("Invalid Move")
        if self.ruleset.check_if_move_into_check(self.board, start_row, start_col, end_row, end_col) == 'invalid move':
            raise ValueError("Invalid Move")
        self.board[start_row][start_col] = "-"
        self.__store_piece_if_struck(end_row, end_col)
        self.board[end_row][end_col] = piece_to_move
        if isinstance(piece_to_move, king.King) and (abs(start_col - end_col) == 2):
            if end_col == 6:
                self.board[end_row][5] = self.board[end_row][7]
                self.board[end_row][7] = '-'
            elif end_col == 2:
                self.board[end_row][3] = self.board[end_row][0]
                self.board[end_row][0] = '-'
        piece_to_move.increment_counter()

        self.ruleset.check_pawn_promotion(self.board, piece_to_move, end_row, end_col)
        return self.ruleset.check_special_events(self.board, piece_to_move, self.game_log)

    def __store_piece_if_struck(self, end_row, end_col):
        if self.board[end_row][end_col] != '-' and self.board[end_row][end_col].colour == 'White':
            self.player_2.store_piece(self.board[end_row][end_col])
            return self.board[end_row][end_col]
        if self.board[end_row][end_col] != '-' and self.board[end_row][end_col].colour == 'Black':
            self.player_1.store_piece(self.board[end_row][end_col])