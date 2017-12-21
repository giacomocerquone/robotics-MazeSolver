"""Main module"""
import os
import time

from world.World2D import World2D

def main():
    """Main function"""
    world = World2D(10, 10)
    world.make_robots()
    world.world_print()
    os.system('cls' if os.name == 'nt' else 'clear')

    while world.food_list:
        for robot in world.robot_list:
            robot.step()
        world.print_ranking()
        world.world_print()
        time.sleep(.5)

        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()
