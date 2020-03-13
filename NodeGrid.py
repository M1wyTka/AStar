from enum import Enum


class Node:
    def __init__(self, x, y, is_walkable):
        self.x = x
        self.y = y
        self.walkable = is_walkable
        self.g = 0
        self.h = 0
        self.neighbours = []
        self.parent = None
        self.heap_index = 0

    def get_f(self):
        return self.g + self.h

    def set_neighbours(self, neighbours):
        self.neighbours = neighbours

    def compare_to(self, node):
        if self.get_f() == node.get_f():
            if self.h == node.h:
                return 0
            elif self.h > node.h:
                return 1
            else:
                return -1
        elif self.get_f() > node.get_f():
            return 1
        else:
            return -1


class Terrain(Enum):
    PLAIN = 0
    OBSTACLE = 1


class NodeGrid:
    def __init__(self, terrain):
        self.path = []
        self.open_set = []
        self.closed_set = []
        self.grid = []

        self.start = None
        self.end = None

        self.set_size(len(terrain[0]), len(terrain))
        self.set_nodes(terrain)

    def set_size(self, width, height):
        self.width = width
        self.height = height

    def set_start(self, x, y):
        self.start = self.grid[y][x]

    def set_end(self, x, y):
        self.end = self.grid[y][x]

    def set_nodes(self, terrain):
        for i in range(self.height):
            self.grid.append([])
            for j in range(self.width):
                cell = terrain[i][j]
                if cell == Terrain.OBSTACLE.value:
                    self.grid[i].append(Node(j, i, False))
                elif cell == Terrain.PLAIN.value:
                    self.grid[i].append(Node(j, i, True))

        for i in range(self.height):
            for j in range(self.width):
                self.set_node_neighbours(self.grid[i][j])

    def set_node_neighbours(self, node):
        neighbours = []
        grid = self.grid
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if (0 <= node.x + j < self.width) and (0 <= node.y + i < self.height):
                    neighbour = grid[node.y + i][node.x + j]
                    neighbours.append(neighbour)
        node.set_neighbours(neighbours)

    def find_path(self):
        open_set = NodeHeap(self.height*self.width)
        closed_set = self.closed_set
        target = self.end
        open_set.add(self.start)
        while open_set.current_item_count > 0:
            current = open_set.pop()
            closed_set.append(current)
            if current == target:
                self.retrace_path()
                return self.path

            for neighbour in current.neighbours:
                if not neighbour.walkable or neighbour in closed_set:
                    continue
                new_cost_to_neighbour = current.g + self.get_distance(current, neighbour)
                if new_cost_to_neighbour < neighbour.g or not open_set.contains(neighbour):
                    neighbour.g = new_cost_to_neighbour
                    neighbour.h = self.get_distance(neighbour, target)
                    neighbour.parent = current

                    if not open_set.contains(neighbour):
                        open_set.add(neighbour)
                    else:
                        open_set.sort_up(neighbour)
        return []

    def retrace_path(self):
        current = self.end
        while not current == self.start:
            self.path.append(current)
            current = current.parent

    def get_distance(self, node_a, node_b):
        distance_x = abs(node_a.x - node_b.x)
        distance_y = abs(node_a.y - node_b.y)
        if distance_x > distance_y:
            return 14*distance_y + 10*(distance_x - distance_y)
        else:
            return 14*distance_x + 10*(distance_y - distance_x)


class NodeHeap:
    def __init__(self, max_size):
        self.nodes = [0 for i in range(max_size)]
        self.current_item_count = 0

    def add(self, node):
        node.heap_index = self.current_item_count
        self.nodes[self.current_item_count] = node
        self.sort_up(node)
        self.current_item_count += 1

    def sort_up(self, node):
        parent_index = int((node.heap_index-1) / 2)
        while True:
            parent_node = self.nodes[parent_index]
            if node.compare_to(parent_node) < 0:
                self.swap(node, parent_node)
            else:
                break
            parent_index = int((node.heap_index-1)/2)

    def sort_down(self, node):
        while True:
            left_child_ind = node.heap_index * 2 + 1
            right_child_ind = node.heap_index * 2 + 2
            swap_ind = 0
            if left_child_ind < self.current_item_count:
                swap_ind = left_child_ind
                if right_child_ind < self.current_item_count:
                    if self.nodes[left_child_ind].compare_to(self.nodes[right_child_ind]) > 0:
                        swap_ind = right_child_ind
                if node.compare_to(self.nodes[swap_ind]) > 0:
                    self.swap(node, self.nodes[swap_ind])
                else:
                    return
            else:
                return

    def contains(self, node):
        return self.nodes[node.heap_index] == node

    def pop(self):
        first_node = self.nodes[0]
        self.current_item_count -= 1
        self.nodes[0] = self.nodes[self.current_item_count]
        self.nodes[0].heap_index = 0
        self.sort_down(self.nodes[0])
        return first_node

    def swap(self, a, b):
        nodes = self.nodes
        nodes[a.heap_index], nodes[b.heap_index] = nodes[b.heap_index], nodes[a.heap_index]
        a.heap_index, b.heap_index = b.heap_index, a.heap_index
