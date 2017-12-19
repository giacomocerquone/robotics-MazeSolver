"""Main module"""
import os
import time

from World2D import World2D

def main():
    """Main function"""
    world = World2D(10, 10)
    world.world_print()
    world.make_robots()
    os.system('cls' if os.name == 'nt' else 'clear')

    for count in range(100):
        time.sleep(1)
        for robot in world.robot_list:
            robot.step()
        world.world_print()
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()
