from piece import Piece

class King(Piece):
    def __init__(self, colour):
        self.colour = colour
        self.name = "King"
        if self.colour == "Black":
            self.symbol = '♚'
        elif self.colour == "White":
            self.symbol = '♔'

    def in_check(self):
        return False

    def illegal_directions(self, board, start_row, start_col, end_row, end_col):
        return any([
            (self.invalid_move_types(start_row, start_col, end_row, end_col)),
            (self.__king_specific_board_constraints(board, start_row, start_col, end_row, end_col))
            ])

    def invalid_move_types(self, start_row, start_col, end_row, end_col):
        if (start_row != end_row and start_col != end_col) and (abs(start_row - end_row) != abs(start_col - end_col)):
            return True
        else:
            return False

    def __king_specific_board_constraints(self, board, start_row, start_col, end_row, end_col):
        piece_to_move = board[start_row][start_col]
        return any([
            (abs(start_row - end_row) > 1),
            (abs(start_col - end_col) > 1),
            (isinstance(board[end_row][end_col], Piece) and board[end_row][end_col].colour == piece_to_move.colour)
            ])
