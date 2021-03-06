from king import King
from piece import Piece
from turn import Turn

class Checkmate:
        def __init__(self, game):
            self.game = game
            self.board = game.board
            if game.p1_turn == True:
                self.current_player = game.player_1.colour
            else:
                self.current_player = game.player_2.colour

        def is_checkmate(self):
            checkmate_evals = []
            for i in range(0,8):
                for j in range(0,8):
                    if isinstance(self.board[i][j], Piece) and self.board[i][j].colour == self.current_player:
                        for sq in self.board[i][j].available_moves(self.board, i, j):
                            checkmate_evals.append(Turn(self.game.ruleset, self.board, self.game.log, self.game.player_1, self.game.player_2).ruleset.check_if_move_into_check(self.board, i, j, sq[0], sq[1]) == 'invalid move')
            return all(checkmate_evals)
