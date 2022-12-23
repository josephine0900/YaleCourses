from Workers import Worker

#! template method pattern for Computer subclasses

class Player:
    """Creates a player to play Santorini."""

    def __init__(self, color):
        self.color = color
        self.score = 0
        if self.color == 'White':
            self.workers = [Worker('A', self, (3, 1)), Worker('B', self, (1, 3))]
        elif self.color == 'Blue':
            self.workers = [Worker('Y', self, (1, 1)), Worker('Z', self, (3, 3))]

    def game_ended(self, space):
        """Check if game has ended by checking the workers' location levels of current player"""

        # check the level of each worker's location
        if space.level_number == 3:
            return True

class Random:
    """Computer player that will randomly choose a move from the set of allowed moves."""

    def __init__(self):
        pass

class Heuristic:
    """Computer player that will assess the available moves and choose the one that it thinks is best based on certain criteria."""

    def __init__(self):
        pass