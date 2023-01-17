import sys
import pygame
from display import Display
from pathfinding import Pathfinder


# Static color values
white = (255, 255, 255)
grey = (128, 128, 128)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
orange = (255, 128, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)


# Creates the display and runs the main loop
def main(rows, columns, cut_corners):
    display = Display(rows, columns, 20)
    pathfinder = Pathfinder(rows, columns, cut_corners)

    running = True

    while running:
        run_mouse(display, pathfinder)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                run_key_input(display, event, pathfinder)

        draw_nodes(display, pathfinder)
        display.draw_grid()
        pygame.display.update()


# Mouse movement and interaction ran every tick
def run_mouse(display, pathfinder):
    mouse_pos = pygame.mouse.get_pos()
    grid_pos = display.get_grid_pos(mouse_pos)

    # Do not allow any mouse configuration when a path is already found
    if not pathfinder.found_path:
        if pygame.mouse.get_pressed()[0]:
            if pathfinder.start is None:
                pathfinder.start = grid_pos
            elif grid_pos != pathfinder.start and pathfinder.target is None:
                pathfinder.target = grid_pos
        elif pygame.mouse.get_pressed()[2]:
            node = pathfinder.world.get_or_create(grid_pos)
            node.passable = False


# Key input on key event
def run_key_input(display, event, pathfinder):
    if event.key == pygame.K_SPACE:
        pathfinder.find_path()
    elif event.key == pygame.K_ESCAPE:
        pathfinder.reset()
    elif event.key == pygame.K_DELETE:
        mouse_pos = pygame.mouse.get_pos()
        grid_pos = display.get_grid_pos(mouse_pos)
        pathfinder.world.remove_node(grid_pos)

        # Also allow clearing start and target using delete
        if pathfinder.start == grid_pos:
            pathfinder.start = None
        if pathfinder.target == grid_pos:
            pathfinder.target = None


# Draws all nodes from a pathfinder on the display
def draw_nodes(display, pathfinder):
    for x in range(display.rows):
        for y in range(display.columns):
            color = white
            coord = (x, y)
            node = pathfinder.world.get_node(coord)

            if coord == pathfinder.start:
                color = red
            elif coord == pathfinder.target:
                color = blue
            elif node is not None:
                color = yellow
                if node.path_part:
                    color = green
                elif not node.passable:
                    color = black
                elif node.visited:
                    color = orange

            display.draw_rectangle(coord, color)


# Only invoke script when running from the main python file
if __name__ == "__main__":
    rows = 40
    columns = 40
    cut_corners = False

    # Either provide no args or all args
    if len(sys.argv) > 1:
        rows = int(sys.argv[1])  # Amount of rows to use
        columns = int(sys.argv[2])  # Amount of columns to use
        cut_corners = sys.argv[3] == 'True'  # If the pathfinder should cut corners and make diagonal paths

    main(rows, columns, cut_corners)


