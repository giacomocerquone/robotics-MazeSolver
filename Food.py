"""Food class"""

import random

class Food:
    """Defines how a Food object is created"""

    def __init__(self, pos, world=None):
        assert isinstance(pos, tuple)
        assert len(pos) == 2

        self.pos = pos
        self.width, self.height = 5, 5
        self.map = [[0 for i in range(self.width)] for j in range(self.height)]
        self.myworld = world

    def get_position(self):
        """Get the position of a robot"""

        return self.pos

    def set_position(self, i, j):
        """Set the position of a robot"""

        self.pos = (i, j)
        self.myworld.change(i, j, 'o')

    def map_print(self):
        """Print the map"""

        for i in range(self.height):
            print(self.map[i])
