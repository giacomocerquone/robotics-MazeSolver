import random
from Robot import Robot

class World2D:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = [ [0 for i in range(self.width)] for j in range(self.height)]
        self.robotList = []
        for i in range(self.height):
            self.matrix[i][random.randint(0, self.width-1)] = '#'
            self.matrix[i][random.randint(0, self.width-1)] = '#'
        for i in range(self.height):
            randomNumber = random.randint(0, self.width-1);
            while self.matrix[i][randomNumber] == "#":
                randomNumber = random.randint(0, self.width-1);
            self.matrix[i][randomNumber] = "R" + i.__str__();

    def worldPrint(self):
        for i in range(self.height):
            print(self.matrix[i])

    def makeRobots(self):
        for i in range(self.height):
            for j in range(self.width):
                if(isinstance(self.matrix[i][j], str) and self.matrix[i][j][0] == 'R'):
                    rob = Robot(self.matrix[i][j], (i,j), self)
                    self.robotList.append(rob)

    def printRobots(self):
        for r in self.robotList:
            print(r)

    def getAround(self, pos):

        '''
        extract of the surroundings
        :param pos: coordinate of the center cell from witch we extract the surroundings
        :return: list of surroundings cells
        '''
        out=[]
        if pos[0]==0:
            out.append(('N', "-"))
        else: out.append(('N', self.matrix[pos[0] - 1] [pos[1]]))
        if pos[0]==self.height-1:
            out.append(('S', "-"))
        else: out.append(('S', self.matrix[pos[0] + 1] [pos[1]]))
        if pos[1]==0:
            out.append(('W', "|"))
        else: out.append(('W', self.matrix[pos[0]] [pos[1]-1]))
        if pos[1]==self.width-1:
            out.append(('E', "|"))
        else: out.append(('E', self.matrix[pos[0]] [pos[1]+1]))

        return out

    def change(self,i,j,name):
        self.matrix[i].pop(j)
        self.matrix[i].insert(j,name)
