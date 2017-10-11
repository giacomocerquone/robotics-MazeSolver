import random

class World2D:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = [ [0 for i in range(self.width)] for j in range(self.height)]
        self.robotList = []
        for i in range(self.height):
            self.matrix[i].insert(random.randint(0, self.width), "#")
            self.matrix[i].insert(random.randint(0, self.width), "#")
        for i in range(self.height):
            randomNumber = random.randint(0, self.width);
            while self.matrix[i][randomNumber] == "#":
                randomNumber = random.randint(0, self.width)
            self.matrix[i].insert(randomNumber, "R" + i.__str__())

    def worldPrint(self):
        for i in range(self.height):
            print(self.matrix[i])

    def makeRobots(self):
        for i in range(self.height):
            for j in range(self.width):
                if(isinstance(self.matrix[i][j], str) and self.matrix[i][j][0] == "R"):
                    rob = Robot(self.matrix[i][j], (i,j))
                    self.robotList.append(rob)

    def printRobots(self):
        for r in self.robotList:
            print(r)

    def getAround(self,pos):

        '''
        extract of the surroundings
        :param pos: coordinate from the central cell which we extract the surroundings
        :return: list of surrounding cells
        '''

        out = [self.matrix[pos[0] - 1][pos[1]], self.matrix[pos[0]][pos[1] + 1], self.matrix[pos[0] + 1][pos[1]],
               self.matrix[pos[0]][pos[1] - 1]]
        return out

class Robot:
    '''
    Defines how a Robot object is created
    '''
    def __init__(self, name, pos):
        assert isinstance(name, str)
        assert isinstance(pos, tuple)
        assert len(pos) == 2

        self.name = name
        self.pos = pos
        self.width,self.height=5,5
        self.map = [[0 for i in range(self.width) ] for j in range(self.height)]
    def getPosition(self):
        return self.pos

    def step(self):
        '''
        This is one step of the robot's life
        :return: None
        '''
        pass

    def __str__(self):
        return self.name + "@" + str(self.pos)

    def perception(self,sensors):
        '''
        build an internal model of the world given current sensors values
        :param sensors:
        :return: nothing, only internal data
        '''
        i=0
        for s in sensors:
            if s[0] == '#':

                if i == 1:
                    self.map[2][3] = '#'
                if i == 2:
                    self.map[3][2] = '#'
                if i == 3:
                    self.map[2][1] = '#'
                if i == 4:
                    self.map[2][1] = '#'
            i+=1


world = World2D(10, 10)
world.worldPrint()
world.makeRobots()
world.printRobots()
print(world.getAround((2,2)))
