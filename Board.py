from Players import Player
from Spaces import Space

class Board:
    """The board to play Santorini."""

    def __init__(self, players):
        """"""
        self.turn_number = 1
        self.players = players
        # 2D array of 5x5 to represent board
        self.board = [[Space(i, j, self) for i in range(5)] for j in range(5)]
        for player in players:
            for worker in player.workers:
                (x, y) = worker.location
                self.board[x][y].set_worker(worker)

    def check_direction(self, worker, direction):
        """Check if the direction is valid."""

        # check if there is a current worker on the space, level 4, or off the board
        dir_list = {'nw':(-1, -1), 'n':(-1, 0) , 'ne':(-1, 1), 'w':(0, -1), 'e':(0, 1), 'sw':(1, -1), 's':(1, 0), 'se':(1, 1)}
        (x, y) = worker.location
        new_x = dir_list[direction][0]
        new_y = dir_list[direction][1]

        if x + new_x < 0 or y + new_y < 0 or self.board[new_x][new_y].level_number == 4 or self.board[new_x][new_y].worker is None:
            return True

    def enumerate_moves(self, worker):
        """Enumerates all possible moves for current player."""

        possible_moves = 0
        (x, y) = worker.location
        dir_list = {'nw', 'n', 'ne', 'w', 'e', 'sw', 's', 'se'}

        for i in dir_list:
            if not self.check_direction(worker, i):
                possible_moves +=1
        return possible_moves

    def apply_move(self, worker, move_direction):
        """Apply the move to selected worker"""

        (x, y) = worker.location

        if move_direction == 'n':
            self.board[x - 1][y].set_worker(worker)
        if move_direction == 'ne':
            self.board[x - 1][y - 1].set_worker(worker)
        if move_direction == 'e':
            self.board[x][y + 1].set_worker(worker)
        if move_direction == 'se':
            self.board[x + 1][y + 1].set_worker(worker)
        if move_direction == 's':
            self.board[x + 1][y].set_worker(worker)
        if move_direction == 'sw':
            self.board[x + 1][y - 1].set_worker(worker)
        if move_direction == 'w':
            self.board[x][y - 1].set_worker(worker)
        if move_direction == 'nw':
            self.board[x - 1][y - 1].set_worker(worker)

        # +1 to the turn number and change current player in Game class
        self.turn_number += 1

    def apply_build(self, worker, build_direction):
        """Build additional level in direction designated by player."""

        (x, y) = worker.location
        
        if build_direction == 'n':
            self.board[x - 1][y].level_number += 1
        if build_direction == 'ne':
            self.board[x - 1][y - 1].level_number += 1
        if build_direction == 'e':
            self.board[x][y + 1].level_number += 1
        if build_direction == 'se':
            self.board[x + 1][y + 1].level_number += 1
        if build_direction == 's':
            self.board[x + 1][y].level_number += 1
        if build_direction == 'sw':
            self.board[x + 1][y - 1].level_number += 1
        if build_direction == 'w':
            self.board[x][y - 1].level_number += 1
        if build_direction == 'nw':
            self.board[x - 1][y - 1].level_number += 1

    def __str__(self):
        """"""
        print("+--+--+--+--+--+\n")
        for i in range(5):
            for j in range(5):
                if (j % 5 == 0):
                    print(self.board[i][j], '|\n') # Space object is being printed is just level number
                    print("+--+--+--+--+--+\n")
                else:
                    print(self.board[i][j], '\n') # Space object is being printed

#         return f"""+--+--+--+--+--+
# |0 |0 |0 |0 |0 |
# +--+--+--+--+--+
# |0 |0Y|0 |0B|0 |
# +--+--+--+--+--+
# |0 |0 |0 |0 |0 |
# +--+--+--+--+--+
# |0 |0A|0 |0Z|0 |
# +--+--+--+--+--+
# |0 |0 |0 |0 |0 |
# +--+--+--+--+--+"""