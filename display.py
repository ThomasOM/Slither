import pygame


# Display containing draw methods for rendering the grid and rectangles
class Display:
    def __init__(self, rows, columns, unit_size):
        self.rows = rows
        self.columns = columns
        self.unit_size = unit_size
        self.window = pygame.display.set_mode((rows * unit_size, columns * unit_size))
        pygame.display.set_caption("Python Pathfinding")

    def draw_grid(self):
        color = (0, 0, 0)

        for i in range(self.columns):
            x = i * self.unit_size
            length = self.rows * self.unit_size
            pygame.draw.line(self.window, color, (x, 0), (x, length))

        for i in range(self.rows):
            y = i * self.unit_size
            length = self.columns * self.unit_size
            pygame.draw.line(self.window, color, (0, y), (length, y))

    def draw_rectangle(self, grid_pos, color):
        x = grid_pos[0]
        y = grid_pos[1]
        pygame.draw.rect(self.window, color, (x * self.unit_size, y * self.unit_size, self.unit_size, self.unit_size))

    def get_grid_pos(self, pixel_pos):
        return pixel_pos[0] // self.unit_size, pixel_pos[1] // self.unit_size
