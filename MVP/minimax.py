from piece import Piece

class Minimax:
        def __init__(self, game, p1_turn):
                self.board = game.board.board
                self.game = game
                if p1_turn == True:
                        self.turn = "White"
                else:
                        self.turn = "Black"
        
        def execute_turn(self):
                return []

        
        def move_value(self):
                return []

                moves = self.available_moves()
                for piece_moves in moves:
                        for move in piece_moves:
                                return "YO"



        def available_moves(self):
                array = []
                for i in range(0,8):
                        for j in range(0,8):
                                if isinstance(self.board[i][j], Piece):
                                        if self.board[i][j].colour == self.turn:
                                                array.append(self.board[i][j].available_moves(self.board, i, j))
                array = list(filter(lambda a: a != [], array)) # removes empty arrays from available moves array
                return array


        