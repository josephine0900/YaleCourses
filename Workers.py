class Worker:
    """"""
    def __init__(self, name, player, location):
        self.name = name
        self.player = player
        self.location = location

    def __str__(self):
        print(self.name)