import pawn
import knight
import game
import pytest
from standard_rules import StandardRules

@pytest.fixture(autouse=True)
def run_before_tests():
        test_game = game.Game('p1', 'p2', ruleset = StandardRules())
        return test_game

class TestKnightightFirstStandardMoves:
        def test_white_knight_left_can_move_forward_left(self, run_before_tests):
                test_game = run_before_tests
                test_game.execute_turn(7,1,5,0)
                assert isinstance(test_game.board[5][0], knight.Knight)
                assert test_game.board[5][0].colour == "White"
                assert test_game.board[7][1] == ("-")

        def test_white_knight_left_can_move_forward_right(self, run_before_tests):
                test_game = run_before_tests
                test_game.execute_turn(7,1,5,2)
                assert isinstance(test_game.board[5][2], knight.Knight)
                assert test_game.board[5][2].colour == "White"
                assert test_game.board[7][1] == ("-")

        def test_white_knight_right_can_move_forward_left(self, run_before_tests):
                test_game = run_before_tests
                test_game.execute_turn(7,6,5,5)
                assert isinstance(test_game.board[5][5], knight.Knight)
                assert test_game.board[5][5].colour == "White"
                assert test_game.board[7][6] == ("-")

        def test_white_knight_right_can_move_forward_right(self, run_before_tests):
                test_game = run_before_tests
                test_game.execute_turn(7,6,5,7)
                assert isinstance(test_game.board[5][7], knight.Knight)
                assert test_game.board[5][7].colour == "White"
                assert test_game.board[7][6] == ("-")

        def test_black_knight_left_can_move_forward_left(self, run_before_tests):
                test_game = run_before_tests
                test_game.execute_turn(6,1,5,1)
                test_game.execute_turn(0,1,2,0)
                assert isinstance(test_game.board[2][0], knight.Knight)
                assert test_game.board[2][0].colour == "Black"
                assert test_game.board[0][1] == ("-")

        def test_black_knight_left_can_move_forward_right(self, run_before_tests):
                test_game = run_before_tests
                test_game.execute_turn(6,1,5,1)
                test_game.execute_turn(0,1,2,2)
                assert isinstance(test_game.board[2][2], knight.Knight)
                assert test_game.board[2][2].colour == "Black"
                assert test_game.board[0][1] == ("-")

        def test_black_knight_right_can_move_forward_left(self, run_before_tests):
                test_game = run_before_tests
                test_game.execute_turn(6,1,5,1)
                test_game.execute_turn(0,6,2,5)
                assert isinstance(test_game.board[2][5], knight.Knight)
                assert test_game.board[2][5].colour == "Black"
                assert test_game.board[0][6] == ("-")

        def test_black_knight_right_can_move_forward_right(self, run_before_tests):
                test_game = run_before_tests
                test_game.execute_turn(6,1,5,1)
                test_game.execute_turn(0,6,2,7)
                assert isinstance(test_game.board[2][7], knight.Knight)
                assert test_game.board[2][7].colour == "Black"
                assert test_game.board[0][6] == ("-")

class TestKnightightCannotLeaveBoard:
        def test_knight_cannot_move_outside_columns(self, run_before_tests):
                test_game = run_before_tests
                test_game.execute_turn(7,1,5,0)
                test_game.execute_turn(1,5,3,5)
                assert test_game.execute_turn(5,0,-1,3) == 'invalid move'

class TestKnightOnlyMovesInLShape:
        def test_knight_moves_in_vertical_L_shape(self, run_before_tests):
                test_game = run_before_tests
                test_game.execute_turn(7,1,5,0)
                test_game.execute_turn(1,5,3,5)
                assert test_game.execute_turn(5,0,6,1) == 'invalid move'

        def test_knight_moves_in_horizontal_L_shape(self, run_before_tests):
                test_game = run_before_tests
                test_game.execute_turn(7,1,5,0)
                test_game.execute_turn(1,5,3,5)
                test_game.execute_turn(5,0,4,2)
                assert test_game.execute_turn(4,2,4,4) == 'invalid move'

        def test_knight_cannot_move_more_than_3_across(self, run_before_tests):
                test_game = run_before_tests
                test_game.execute_turn(7,1,5,0)
                test_game.execute_turn(1,5,3,5)
                test_game.execute_turn(5,0,4,2)
                assert test_game.execute_turn(4,2,3,5) == 'invalid move'

        def test_knight_cannot_move_more_than_3_forward(self, run_before_tests):
                test_game = run_before_tests
                test_game.execute_turn(7,1,5,0)
                test_game.execute_turn(1,5,3,5)
                assert test_game.execute_turn(5,0,2,1) == 'invalid move'

class TestKnightStriking:
        def test_knight_can_strike(self, run_before_tests):
                test_game = run_before_tests
                test_game.execute_turn(7,1,5,0)
                test_game.execute_turn(1,3,2,3)
                test_game.execute_turn(5,0,3,1)
                assert isinstance(test_game.board[3][1], knight.Knight)

        def test_knight_cannot_strike_own_piece(self, run_before_tests):
                test_game = run_before_tests
                test_game.execute_turn(7,1,5,0)
                test_game.execute_turn(1,3,2,3)
                test_game.execute_turn(6,2,4,2)
                test_game.execute_turn(1,5,2,5)
                assert test_game.execute_turn(5,0,4,2) == 'invalid move'
