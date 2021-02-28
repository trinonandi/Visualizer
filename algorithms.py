from queue import PriorityQueue
import pygame


def h(p1, p2):
    """
    heuristic function that calculates the manhattan distance
    :param p1: point 1 having (x,y) coordinates
    :param p2: point 2 having (x,y) coordinates
    :return: the manhattan distance between them
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def a_star(draw, grid, start, end):
    """
    a function to evaluate the A* search algorithm
    :param draw: a function that refreshes the pygame window every time a node's color is changed
    :param grid: the list representation of the graph
    :param start: starting node
    :param end: goal node
    :return: boolean True if a path exists and False if no path exists
    """
    count = 0
    heap = PriorityQueue()
    heap.put((0, count, start))
    open_set = {start}
    path_dict = dict()

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    while not heap.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = heap.get()[2]  # returns the Node object from the tuple
        open_set.remove(current)

        if current == end:  # goal node found
            reconstruct_path(path_dict, end, draw)
            # remaking the start and end node as they will be removed by reconstruct_path()
            end.make_end()
            start.make_start()
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbour]:  # open the neighbour
                path_dict[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())

                if neighbour not in open_set:
                    count += 1
                    heap.put((f_score[neighbour], count, neighbour))
                    open_set.add(neighbour)
                    neighbour.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def reconstruct_path(path_dict, current, draw):
    """
    backtracks through the path_dict and draws the path
    :param path_dict: the dict having all the path nodes from start to goal
    :param current: current node
    :param draw: a function that refreshes the pygame window every time a node's color is changed
    :return: None
    """
    while current in path_dict:
        current = path_dict[current]
        current.make_path()
        draw()


def breadth_first_search(draw, start, end):
    queue = [start]
    parent = {}
    while len(queue) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.pop(0)
        if current == end:
            animate(parent, start, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbour in current.neighbours:
            if current not in queue:
                parent[neighbour] = current
                queue.append(neighbour)
                if current != start:
                    current.make_open()

        draw()
        if current != start:
            current.make_closed()


def animate(path_list, start, end, draw):
    path = [end]
    while path[-1] != start:
        node = path_list[path[-1]]
        path.append(node)
        node.make_path()
        draw()