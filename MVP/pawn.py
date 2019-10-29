class Pawn:
        def __init__(self, colour):
                self.colour = colour
                self.name = 'p'
        
        def illegal_directions(self, start_row, start_col, end_row, end_col):
                return any([self.colour == "Black" and end_row > start_row,
                        self.colour == "White" and end_row < start_row, 
                        start_row == end_row, # cannot move sideways
                        abs(start_row - end_row) > 2, # cannot move more than 2 spaces
                        (start_row != 6 and start_row != 1) and abs(start_row - end_row) >= 2, # cannot move 2 spaces after 1st move
                        abs(start_col - end_col) > 1 # can't move diagonally more than 1 space
                        ]
                        )