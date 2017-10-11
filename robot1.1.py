import random

class World2D:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = [ [0 for i in range(self.width)] for j in range(self.height)]
        self.robotList = []
        for i in range(self.height):
            self.matrix[i].insert(random.randint(0, self.width), '#')
            self.matrix[i].insert(random.randint(0, self.width), '#')
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
            out.append(('E', "|"))
        else: out.append(('E', self.matrix[pos[0]] [pos[1]+1]))
        if pos[1]==self.width-1:
            out.append(('W', "|"))
        else: out.append(('S', self.matrix[pos[0]] [pos[1]-1]))

        return out

    def change(self,i,j,name):
        self.matrix[i].pop(j)
        self.matrix[i].insert(j,name)

class Robot:

    '''
    Defines how a Robot object is created
    '''
    def __init__(self, name, pos, world=None):
        assert isinstance(name, str)
        assert isinstance(pos, tuple)
        assert len(pos) == 2

        self.name = name
        self.pos = pos
        self.width, self.height = 5, 5
        self.map = [[0 for i in range(self.width)] for j in range(self.height)]
        self.myworld = world

    def getPosition(self):
        return self.pos

    def setPosition(self,i,j):
        self.pos = (i,j)
        world.change(i,j,self.name)


    def mapPrint(self):
        for i in range(self.height):
            print(self.map[i])

    def step(self):

        '''
        This is one step of the robot's life
        :return: None
        '''
        self.sense()
        self.act(self.think())

    def sense(self):
        self.perception(self.myworld.getAround(self.getPosition()))


    def __str__(self):
        return self.name + "@" + str(self.pos)


    def perception(self, sensors):

        '''
        Build an internal model of the world given current sensor values
        :param sensors:
        :return: nothing, only internal data
        '''
        for s in sensors:
            if s[0] == 'N': self.map[1][2] = s[1]
            if s[0] == 'S': self.map[3][2] = s[1]
            if s[0] == 'W': self.map[2][1] = s[1]
            if s[0] == 'E': self.map[2][1] = s[1]
        self.mapPrint();

    def think(self):
        '''
        Analize his own map and decide where he can move
        :return N S E W or Blocked:
        '''
        out=[]
        if self.map[1][2] == 0:
            out.append('N')
        if self.map[3][2] == 0:
            out.append('S')
        if self.map[2][1] == 0:
            out.append('W')
        if self.map[2][3] == 0:
            out.append('E')
        if len(out) == 0:
            out.append('X')

        return out[random.randint(0,len(out)-1)]

    def act(self,move):
        '''
        Moves the robot into the map
        :param move: the position (N,S,E,W) or the Blocked status(X)
        :return: none
        '''
        print(self.name)
        print(move)
        if move == 'N':
            world.change(self.pos[0],self.pos[1],0)
            self.setPosition(self.pos[0]-1,self.pos[1])
        elif move == 'S':
            world.change(self.pos[0],self.pos[1],0)
            self.setPosition(self.pos[0]+1,self.pos[1])
        elif move == 'W':
            world.change(self.pos[0],self.pos[1],0)
            self.setPosition(self.pos[0],self.pos[1]-1)
        elif move == 'E':
            world.change(self.pos[0],self.pos[1],0)
            self.setPosition(self.pos[0],self.pos[1]+1)
        elif move == 'X':
            print("porca merda, non posso muovermi")



world = World2D(10, 10)
world.worldPrint()
world.makeRobots()
world.printRobots()
for r in world.robotList:
    r.step()

world.worldPrint()
