from World2D import World2D

def main():
    world = World2D(10, 10)
    world.worldPrint()
    world.makeRobots()
    world.printRobots()

    for r in world.robotList:
        r.step()
    world.printRobots()
    world.worldPrint()

if __name__ == "__main__": main()
