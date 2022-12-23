import sys 
from Board import Board
from Players import Player

class Game:
    
    def __init__(self):
        """Create the two players and a board"""

        self.curr_player = self.player_one
        self.player_one = Player('White')
        self.player_two = Player('Blue')
        self.board = Board([self.player_one, self.player_two])

    def play_game(self):
        """Begin playing Santorini with two players"""

        while True:
            # Start turn and print out board, turn and current player to stdout
            print(self.board)
            print('Turn: {}, {} ({}{})\n', self.board.turn_number, self.curr_player.color, self.curr_player.workers[0].name, self.curr_player.workers[1].name)

            #! enumerating all possible moves for current player --> if workers cannot move then curr_player loses

            #validate if the game has ended
            (x, y) = self.curr_player.workers[0].location
            (a, b) = self.curr_player.workers[1].location

            if self.curr_player.game_ended(self.board[x][y]) or self.curr_player.game_ended(self.board[a][b]) or (self.board.enumerate_moves(self.curr_player.workers[0]) == 0 and self.board.enumerate_moves(self.curr_player.workers[1]) == 0):
                print('{self.curr_player.color} has won\n'.lower())
                sys.exit(0)

            # Prompt user to select a worker to move
            while True: #! what happens if the chosen worker cannot do any more moves
                worker = input("Select a worker to move\n")
                if worker != 'A' or 'B' or 'Y' or 'Z':
                    print('Not a valid worker\n')
                    continue
                if worker == ('A' or 'B' and self.curr_player != 'White') or ('Y' or 'Z' and self.curr_player != 'Blue'):
                    print('That is not your worker\n')
                    continue
                break
            
            # Prompt user to select direction to move in
            while True:
                move_direction = input("Select a direction to move (n, ne, e, se, s, sw, w, nw)")
                if move_direction != 'n' or 'ne' or 'e' or 'se' or 's' or 'sw' or 'w' or 'nw':
                    print('Not a valid direction\n')
                    continue
                if self.board.check_direction(move_direction):
                    print('Cannot move {move_direction}\n')
                    continue
                break
            
            # Prompt user to select a direction to build in
            while True:
                build_direction = input("Select a direction to build (n, ne, e, se, s, sw, w, nw)")
                if build_direction != 'n' or 'ne' or 'e' or 'se' or 's' or 'sw' or 'w' or 'nw':
                    print('Not a valid direction\n')
                if self.board.check_direction(build_direction):
                    print('Cannot build {build_direction}\n')
                    continue
                break
            
            # Apply move to player based on CLI arguments
            self.board.apply_move(worker, move_direction)
            self.board.apply_build(worker, build_direction)

            # change to other player for next turn
            # if 
            # self.curr_player = 