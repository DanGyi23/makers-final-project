import pytest
from piece import Piece
from king import King
from game import Game
from checkmate import Checkmate
from standard_rules import StandardRules

@pytest.fixture(autouse=True)
def run_before_tests():
        test_game = Game("p1", "p2", ruleset = StandardRules())
        test_checkmate = Checkmate(test_game)
        return test_checkmate

class TestCheckmate:

        def test_king_is_not_in_checkmate(self, run_before_tests):
                test_checkmate = run_before_tests
                assert test_checkmate.is_checkmate() == False

        def test_king_is_not_in_checkmate(self, run_before_tests):
                test_checkmate = run_before_tests
                test_checkmate.game.execute_turn(6,5,5,5)
                test_checkmate.game.execute_turn(1,4,3,4)
                test_checkmate.game.execute_turn(6,6,4,6)
                assert test_checkmate.is_checkmate() == False

        def test_king_is_not_in_checkmate2(self, run_before_tests):
                test_checkmate = run_before_tests
                test_checkmate.game.execute_turn(6,2,4,2)
                test_checkmate.game.execute_turn(1,4,2,4)
                test_checkmate.game.execute_turn(7,3,5,1)
                test_checkmate.game.execute_turn(0,3,4,7)
                assert test_checkmate.is_checkmate() == False

        def test_king_is_not_in_checkmate3(self, run_before_tests):
                test_checkmate = run_before_tests
                test_checkmate.game.execute_turn(6,4,4,4)
                test_checkmate.game.execute_turn(1,5,3,5)
                test_checkmate.game.execute_turn(4,4,3,5)
                test_checkmate.game.execute_turn(1,7,3,7)
                test_checkmate.game.execute_turn(3,5,2,5)
                test_checkmate.game.execute_turn(3,7,4,7)
                test_checkmate.game.execute_turn(2,5,1,5)
                test_checkmate.game.execute_turn(0,4,1,5)
                print(test_checkmate.game.board)
                assert test_checkmate.is_checkmate() == False

        # fool's mate
        def test_fools_mate_is_checkmate(self, run_before_tests):
                test_checkmate = run_before_tests
                print(test_checkmate.game.ruleset)
                print(test_checkmate.game.board)
                test_checkmate.game.execute_turn(6,5,5,5)
                assert test_checkmate.is_checkmate() == False
                test_checkmate.game.execute_turn(1,4,3,4)
                assert test_checkmate.is_checkmate() == False
                test_checkmate.game.execute_turn(6,6,4,6)
                assert test_checkmate.is_checkmate() == False
                test_checkmate.game.execute_turn(0,3,4,7)
                assert test_checkmate.is_checkmate() == True

        # scholar's mate
        def test_scholars_mate_is_checkmate(self, run_before_tests):
                test_game1 = Game("p1", "p2", ruleset = StandardRules())
                test_game1.execute_turn(6,4,4,4)
                test_game1.execute_turn(1,4,3,4)
                test_game1.execute_turn(7,5,4,2)
                test_game1.execute_turn(1,0,2,0)
                test_game1.execute_turn(7,3,5,5)
                test_game1.execute_turn(2,0,3,0)
                test_game1.execute_turn(5,5,1,5)
                assert Checkmate(test_game1).is_checkmate() == True
