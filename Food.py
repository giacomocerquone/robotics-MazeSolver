"""Food class"""

class Food:
    """Defines how a Food object is created"""

    def __init__(self, pos, world=None):
        assert isinstance(pos, tuple)
        assert len(pos) == 2

        self.pos = pos
        self.width, self.height = 5, 5
        self.map = [[0 for i in range(self.width)] for j in range(self.height)]
        self.myworld = world
