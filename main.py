"""Main module"""
import time
from World2D import World2D

def main():
    """Main function"""
    world = World2D(10, 10)

    world.make_robots()
    world.make_foods()
    world.world_print()

    while world.food_list:
        world.print_robots()
        for robot in world.robot_list:
            robot.step()
        world.print_ranking()
        world.world_print()
        print(world.food_list)
        # time.sleep(5)

if __name__ == "__main__":
    main()
