from Players import Player
from Board import Board
from game import Game

class SantoriniCLI:
    """Display a board and prompt the user to make moves."""

    def __init__(self):
        self.game = Game()
        
    # def display_board(self):
    #     print(self._board)

    def run(self):
        """"""
        self.game.play_game()

if __name__ == "__main__":
    SantoriniCLI().run()