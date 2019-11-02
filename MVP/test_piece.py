import pytest
from piece import Piece
import chessboard
import king

@pytest.fixture(autouse=True)
def run_before_tests():
        test_game = Game("p1", "p2")

class TestAvailableMoves:
        def test_pawn_has_only_2_available_start_moves(self, run_before_tests):
                test_game = run_before_tests
                assert test_game.board.board[6][0].available_moves(test_game.board.board, 6, 0) == [[4,0],[5,0]]

        def test_knight_has_only_2_available_start_moves(self, run_before_tests):
                test_game = run_before_tests
                assert test_game.board[0][1].available_moves(test_game.board, 0, 1) == [[2,0],[2,2]]

        def test_Queen_has_only_2_available_moves_forward(self, run_before_tests):
                test_game = run_before_tests
                test_game.execute_turn(6, 3, 4, 3)
                test_game.execute_turn(1, 5, 3, 5)
                assert test_game.board[7][3].available_moves(test_game.board, 7, 3) == [[5,3],[6,3]]

        def test_Queen_has_only_4_available_moves_diagonally(self, run_before_tests):
                test_game = run_before_tests
                test_game.execute_turn(6, 4, 4, 4)
                test_game.execute_turn(1, 5, 3, 5)
                # print(test_game.board[7][3].available_moves(test_game.board, 7, 3))
                assert test_game.board[7][3].available_moves(test_game.board, 7, 3) == [[3,7],[4,6],[5,5],[6,4]]