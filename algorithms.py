from queue import PriorityQueue
import bidirectional
import pygame

CLOCK_DELAY = 15


def h(p1, p2):
    """
    heuristic function h(x) that calculates the manhattan distance
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
    it is an informed search algorithm with f(x) = g(x) + h(x) where g(x) is the path cost
    we will use a heap to sort the node with respect to the f(x) score
    it guarantees the shortest path and is a very efficient algorithm
    :param draw: a function that refreshes the pygame window every time a node's color is changed
    :param grid: the list representation of the graph
    :param start: starting node
    :param end: goal node
    :return: boolean True if a path exists and False if no path exists
    """
    count = 0
    heap = PriorityQueue()
    heap.put((0, count, start))
    open_list = []
    path_dict = {}

    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    while not heap.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        current = heap.get()[2]  # returns the Node object from the tuple

        if current == end:  # goal node found
            animate(path_dict, start, end, draw)
            # remaking the start and end node as they will be removed by reconstruct_path()
            end.make_end()
            start.make_start()
            return True

        for neighbour in current.neighbours:
            if neighbour in open_list:
                continue
            path_dict[neighbour] = current
            if neighbour != start:
                count += 1
                temp_g_score = g_score[current] + 1
                g_score[neighbour] = temp_g_score  # g(x)
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())  # f(x) = g(x) + h(x)
                heap.put((f_score[neighbour], count, neighbour))
                open_list.append(neighbour)
                neighbour.make_open()

        pygame.time.delay(CLOCK_DELAY)
        draw()

        if current != start:
            current.make_closed()

    return False


def dijkstra(draw, grid, start, end):
    """
    a function to implement dijkstra's algorithm
    it is a blind search technique and the father of all pathfinding algorithms
    we have used a heap to implement it
    it guarantees shortest path
    :param draw: a function that refreshes the pygame window every time a node's color is changed
    :param grid: the list representation of the graph
    :param start: starting node
    :param end: goal node
    :return: boolean True if a path exists and False if no path exists
    """
    distance = {node: float("inf") for row in grid for node in row}
    distance[start] = 0
    path_dict = {}
    heap = PriorityQueue()
    heap.put((0, start))
    while not heap.empty():
        current = heap.get()[1]
        if current == end:
            animate(path_dict, start, end, draw)
            start.make_start()
            end.make_end()
            return True

        for neighbour in current.neighbours:

            if distance[neighbour] > distance[current] + 1:
                path_dict[neighbour] = current
                distance[neighbour] = distance[current] + 1
                heap.put((distance[neighbour], neighbour))
                neighbour.make_open()

        draw()
        if current != start:
            current.make_closed()

    return False


def breadth_first_search(draw, start, end):
    """
    a function to evaluate BFS algorithm
    it is a blind search algorithm
    we will use a queue to implement it
    it guarantees shortest path
    :param draw: a function that refreshes the pygame window every time a node's color is changed
    :param start: starting node
    :param end: goal node
    :return: boolean True if a path exists and False if no path exists
    """
    queue = [start]
    path_dict = {}
    open_list = []
    while len(queue) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        current = queue.pop(0)
        if current == end:
            animate(path_dict, start, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbour in current.neighbours:  # iterating over neighbours
            if current not in queue:
                # opening a neighbour
                if neighbour in open_list:
                    # if neighbour is already opened, then no need to open it anymore
                    continue
                path_dict[neighbour] = current  # making current as parent of all neighbours
                queue.append(neighbour)
                if neighbour != start and neighbour != end:
                    neighbour.make_open()
                    open_list.append(neighbour)

        pygame.time.delay(CLOCK_DELAY)
        draw()
        if current != start:
            current.make_closed()

    return False


def depth_first_search(draw, start, end):
    """
    a function to evaluate DFS algorithm
    it is a blind search algorithm
    we will use stack to implement it
    it does not guarantee shortest path
    :param draw: a function that refreshes the pygame window every time a node's color is changed
    :param start: starting node
    :param end: goal node
    :return: boolean True if a path exists and False if no path exists
    """
    stack = [start]
    path_dict = {}
    open_list = []

    while len(stack) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        current = stack.pop()

        if current == end:
            animate(path_dict, start, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbour in current.neighbours:  # iterating over neighbours
            if current not in stack:
                # opening a neighbour
                if neighbour in open_list:
                    # if neighbour is already opened, then no need to open it anymore
                    continue
                path_dict[neighbour] = current  # making current as parent of all neighbours
                stack.append(neighbour)
                if neighbour != start and neighbour != end:
                    neighbour.make_open()
                    open_list.append(neighbour)

        pygame.time.delay(CLOCK_DELAY)
        draw()
        if current != start:
            current.make_closed()

    return False


def greedy_best_first(draw, grid, start, end):
    """
    a function to implement greedy best first search algorithm
    it is an informed search algorithm with f(x) = h(x)
    we will implement it using a heap where the nodes will be sorted with respect to lowest heuristic score
    it is called greedy because it always chooses the node with lowest heuristic score
    it does not guarantee shortest path
    :param draw: a function that refreshes the pygame window every time a node's color is changed
    :param grid: the list representation of the graph
    :param start: starting node
    :param end: goal node
    :return: boolean True if a path exists and False if no path exists
    """
    heap = PriorityQueue()
    heap.put((0, start))
    open_list = []
    path_dict = dict()

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    while not heap.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        current = heap.get()[1]  # returns the Node object from the tuple

        if current == end:  # goal node found
            animate(path_dict, start, end, draw)
            # remaking the start and end node as they will be removed by reconstruct_path()
            end.make_end()
            start.make_start()
            return True

        for neighbour in current.neighbours:
            if neighbour in open_list:
                continue
            path_dict[neighbour] = current
            if neighbour != start:
                f_score[neighbour] = h(neighbour.get_pos(), end.get_pos())  # f(x) = g(x) + h(x)
                heap.put((f_score[neighbour], neighbour))
                open_list.append(neighbour)
                neighbour.make_open()

        pygame.time.delay(CLOCK_DELAY)
        draw()

        if current != start:
            current.make_closed()

    return False


def bidirectional_search(draw, grid, start, end):
    """
    a function to implement Blind Bidirectional Search by BFS algorithm
    it is uninformed and uses BFS from both the goal and start node simultaneously
    it stops when the start search path and goal search path collides
    it guarantees shortest path

    It uses the bidirectional.py module's BidirectionalSearch class
    The actual algorithm implementation is written in that module
    :param draw: a function that refreshes the pygame window every time a node's color is changed
    :param grid: the list representation of the graph
    :param start: starting node
    :param end: goal node
    :return: boolean True if a path exists and False if no path exists
    """
    bs = bidirectional.BidirectionalSearch(draw, grid, start, end)
    return bs.search()


def bidirectional_a_star_search(draw, grid, start, end):
    """
    a function to implement bidirectional A* search algorithm
    it uses heuristic function so it is informed and takes the best of A* search and bidirectional search
    it guarantees shortest path

    It uses the bidirectional.py module's InformedBidirectionalSearch class
    The actual algorithm implementation is written in that module
    :param draw: a function that refreshes the pygame window every time a node's color is changed
    :param grid: the list representation of the graph
    :param start: starting node
    :param end: goal node
    :return: boolean True if a path exists and False if no path exists
    """
    bs = bidirectional.InformedBidirectionalSearch(draw, grid, start, end)
    return bs.a_star_search()


def bidirectional_greedy_search(draw, grid, start, end):
    """
    a function to implement bidirectional greedy best first search
    it uses heuristic function to perform best first search from start and goal node simultaneously
    it does not guarantee shortest path

    It uses the bidirectional.py module's InformedBidirectionalSearch class
    The actual algorithm implementation is written in that module
    :param draw: a function that refreshes the pygame window every time a node's color is changed
    :param grid: the list representation of the graph
    :param start: starting node
    :param end: goal node
    :return: boolean True if a path exists and False if no path exists
    """
    bs = bidirectional.InformedBidirectionalSearch(draw, grid, start, end)
    return bs.greedy_search()


def animate(path_dict, start, end, draw):
    """
    a function that animates the path by backtracking the path_dict
    :param path_dict: a dictionary that holds the node as key and its parent as value
    :param start: starting node
    :param end: goal node
    :param draw: a function that refreshes the pygame window every time a node's color is changed
    :return: None
    """
    path = [end]
    while path[-1] != start:
        node = path_dict[path[-1]]
        path.append(node)

    path = path[::-1]
    for node in path:
        node.make_path()
        pygame.time.delay(CLOCK_DELAY)
        draw()
