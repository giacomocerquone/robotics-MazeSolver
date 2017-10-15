"""Main module"""

from World2D import World2D

def main():
    """Main function"""
    world = World2D(10, 10)
    world.world_print()
    world.make_robots()
    world.print_robots()

    for robot in world.robot_list:
        robot.step()
    world.print_robots()
    world.world_print()

if __name__ == "__main__":
    main()
