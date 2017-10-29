"""Main module"""
from world.World2D import World2D

def main():
    """Main function"""
    world = World2D(10, 10)

    world.make_robots()
    world.world_print()

    while world.food_list:
        world.print_robots()
        for robot in world.robot_list:
            robot.step()
        world.print_ranking()
        world.world_print()

if __name__ == "__main__":
    main()
