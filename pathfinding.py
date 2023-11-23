import math
from queue import PriorityQueue


# Simple hash for 2d coordinate to store in dictionary
def hash_coord(coord):
    return int(coord[0]) << 16 | int(coord[1])


# Retraces the path from the target node back to the start node after a path has been found
def retrace_path(start_node, target_node):
    current_node = target_node

    while current_node != start_node:
        current_node.path_part = True

        if current_node.parent is not None:
            current_node = current_node.parent


class Pathfinder:
    """
    Simple pathfinder implementation using the A* algorithm
    :param rows: Amount of rows for node dimension
    :param columns: Amount of columns for node dimension
    :param cut_corners: If the pathfinder is allowed to cut corners by traveling diagonally
    """

    def __init__(self, rows, columns, cut_corners):
        self.rows = rows
        self.columns = columns
        self.cut_corners = cut_corners
        self.world = World()
        self.start = None
        self.target = None
        self.found_path = False

    def find_path(self):
        """
        Finds the path within the node world using the A* algorithm
        """
        self.found_path = True
        start_node = self.world.get_or_create(self.start)
        target_node = self.world.get_or_create(self.target)

        start_node.g_cost = 0.0
        start_node.h_cost = 0.0

        #
        open_nodes = PriorityQueue()
        open_set = {start_node}

        open_nodes.put((start_node.get_f_cost(), start_node))

        while open_nodes.qsize() > 0:
            current_node = open_nodes.get()[1]
            open_set.remove(current_node)
            current_node.visited = True

            if current_node == target_node:
                retrace_path(start_node, target_node)
                return

            self.scan_neighbors(open_nodes, open_set, current_node, target_node)

    def scan_neighbors(self, open_nodes, open_set, current_node, target_node):
        """
        Scans neighbours of a node and adds them to the open nodes and set while updating their costs
        :param open_nodes: open node priority queue
        :param open_set: set storing hashes for
        :param current_node: current node to get the neighbours for
        :param target_node: target node to navigate to
        """
        current_coord = current_node.coord
        for x in range(max(0, current_coord[0] - 1), min(self.rows, current_coord[0] + 2)):
            for y in range(max(0, current_coord[1] - 1), min(self.columns, current_coord[1] + 2)):
                # No reason to check the same node
                neighbor_coord = (x, y)
                if neighbor_coord == current_coord:
                    continue

                # Make sure cutting corners is allowed
                if not self.cut_corners and abs(current_coord[0] - x) + abs(current_coord[1] - y) == 2:
                    continue

                neighbor_node = self.world.get_or_create((x, y))
                if neighbor_node.visited or not neighbor_node.passable:
                    continue

                calculated_g = current_node.g_cost + current_node.get_cost_to(neighbor_node)
                if calculated_g < neighbor_node.g_cost:
                    neighbor_node.g_cost = calculated_g
                    neighbor_node.parent = current_node
                    neighbor_node.h_cost = neighbor_node.get_cost_to(target_node)

                    if neighbor_node not in open_set:
                        open_nodes.put((neighbor_node.get_f_cost(), neighbor_node))
                        open_set.add(neighbor_node)

    def reset(self):
        """
        Resets the pathfinder, clearing the node world, the start and target, and marks it as not having found a path
        """
        self.world.clear()
        self.start = None
        self.target = None
        self.found_path = False


class World:
    def __init__(self):
        self.nodes = dict()

    def get_node(self, coord):
        hashed = hash_coord(coord)
        return self.nodes.get(hashed)

    def get_or_create(self, coord):
        hashed = hash_coord(coord)

        if hashed not in self.nodes:
            self.nodes[hashed] = Node(coord)

        return self.nodes.get(hashed)

    def remove_node(self, coord):
        hashed = hash_coord(coord)
        if hashed in self.nodes:
            del self.nodes[hashed]

    def clear(self):
        self.nodes.clear()


class Node:
    def __init__(self, coord):
        self.coord = coord
        self.visited = False
        self.parent = None
        self.passable = True
        self.path_part = False
        self.g_cost = float("inf")
        self.h_cost = float("inf")

    def get_f_cost(self):
        return self.g_cost + self.h_cost

    def get_cost_to(self, other):
        dx = float(self.coord[0] - other.coord[0])
        dy = float(self.coord[1] - other.coord[1])
        return math.sqrt(dx * dx + dy * dy)

    def __lt__(self, other):
        return False  # Need to override this because of use in priority queue
