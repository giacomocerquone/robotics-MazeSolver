"""World representation"""

import random
from robot.Robot import Robot

class World2D:
    """World representation class"""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = [[0 for i in range(self.width)] for j in range(self.height)]
        self.robot_list = []
        self.food_list = 0
        # Adding walls char in matrix
        for i in range(self.height):
            self.matrix[i][random.randint(0, self.width-1)] = '#'
            self.matrix[i][random.randint(0, self.width-1)] = '#'
        # Adding robot char in matrix
        for i in range(self.height):
            random_n = random.randint(0, self.width-1)
            while self.matrix[i][random_n] == "#":
                random_n = random.randint(0, self.width-1)
            self.matrix[i][random_n] = "R" + i.__str__()
        # Adding food char in matrix
        for i in range(self.height):
            random_n = random.randint(0, self.width-1)
            while (not self.matrix[i][random_n] == 0
                   or (i > 0 and random_n > 0 and self.matrix[i-1][random_n] == "#" and self.matrix[i][random_n-1] == "#")
                   or (i > 0 and random_n < self.width-1 and self.matrix[i-1][random_n] == "#" and self.matrix[i][random_n+1] == "#")
                   or (i < self.height-1 and random_n > 0 and self.matrix[i+1][random_n] == "#" and self.matrix[i][random_n-1] == "#")
                   or (i < self.height-1 and random_n < self.width-1 and self.matrix[i+1][random_n] == "#" and self.matrix[i][random_n+1] == "#")):
                random_n = random.randint(0, self.width-1)
            self.matrix[i][random_n] = "o"
            self.food_list += 1

    def world_print(self):
        """Print the world"""

        for i in range(self.height):
            print('\t'.join(str(v) for v in self.matrix[i]))

    def make_robots(self):
        """Instantiate the robots"""

        for i in range(self.height):
            for j in range(self.width):
                if isinstance(self.matrix[i][j], str) and self.matrix[i][j][0] == 'R':
                    types = ['smart', 'dumb']
                    rob = Robot(self.matrix[i][j], (i, j), random.choice(types), self)
                    self.robot_list.append(rob)

    def print_robots(self):
        """Print the robots"""
        for robot in self.robot_list:
            print(robot)

    def print_ranking(self):
        """Print the ranking"""
        ranking = dict()
        for robot in self.robot_list:
            ranking[robot.name] = str(robot.points) + ', ' + str(robot.kind)
        sorted_robots = sorted(ranking, key=ranking.get, reverse=True)
        print("\nRanking")
        for key in sorted_robots:
            print(key, ranking[key])
        print("\n")

    def get_around(self, pos):
        '''
        extract of the surroundings
        :param pos: coordinate of the center cell from witch we extract the surroundings
        :return: list of surroundings cells
        '''

        out = []
        if pos[0] == 0:
            out.append(('N', "-"))
        else:
            out.append(('N', self.matrix[pos[0] - 1][pos[1]]))
        if pos[0] == self.height-1:
            out.append(('S', "-"))
        else:
            out.append(('S', self.matrix[pos[0] + 1][pos[1]]))
        if pos[1] == 0:
            out.append(('W', "|"))
        else:
            out.append(('W', self.matrix[pos[0]][pos[1]-1]))
        if pos[1] == self.width-1:
            out.append(('E', "|"))
        else:
            out.append(('E', self.matrix[pos[0]][pos[1]+1]))

        return out

    def change(self, i, j, name):
        """Swap the object in i, j with the object in name"""
        self.matrix[i].pop(j)
        self.matrix[i].insert(j, name)
