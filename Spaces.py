from Workers import Worker

class Space:
    def __init__(self, x, y, board):
        self.level_number = 0
        self.worker = None
        self.location = (x, y)
        self.board = board
        
    def set_worker(self, worker):
        self.worker = worker

    def __str__(self):
        if self.worker:
            print('|' + str(self.level_number) + self.worker)
        else:
            print('|' + str(self.level_number) + ' ')