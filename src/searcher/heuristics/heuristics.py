import numpy as np
from itertools import permutations
from collections import deque

from src.model.board import Board


def manhattan_distance(board: Board, boxes: tuple) -> float:
    distance = 0.0
    complete = set(board.destinations) & set(boxes)
    open_boxes = sorted(list(set(boxes).difference(complete)))
    open_destinations = sorted(list(set(board.destinations).difference(complete)))

    for i in range(len(open_boxes)):
        distance += np.abs(open_boxes[i][0] - open_destinations[i][0]) + \
                    np.abs(open_boxes[i][1] - open_destinations[i][1])

    return distance

def bfs_distance(board: Board, start: tuple, goal: tuple) -> float:
    if start == goal:
        return 0
    visited = set()
    queue = deque([(start, 0)])
    walls = set(board.walls)
    while queue:
        (y, x), dist = queue.popleft()
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            ny, nx = y + dy, x + dx
            if (ny, nx) == goal:
                return dist + 1
            if (ny, nx) in walls or (ny, nx) in visited:
                continue
            visited.add((ny, nx))
            queue.append(((ny, nx), dist + 1))
    return 9999

def wall_aware_manhattan_distance(board: Board, boxes: tuple) -> float:
    boxes = list(boxes)
    goals = list(board.destinations)
    
    complete = set(goals) & set(boxes)
    open_boxes = [b for b in boxes if b not in complete]
    open_goals = [g for g in goals if g not in complete]
    if not open_boxes:
        return 0.0

    
    cost_matrix = np.zeros((len(open_boxes), len(open_goals)))
    for i, box in enumerate(open_boxes):
        for j, goal in enumerate(open_goals):
            cost_matrix[i, j] = bfs_distance(board, box, goal)

    
    min_total = float('inf')
    for perm in permutations(range(len(open_goals)), len(open_boxes)):
        total = sum(cost_matrix[i, perm[i]] for i in range(len(open_boxes)))
        if total < min_total:
            min_total = total

    return min_total

def max_distance(board: Board, boxes: tuple) -> float:
    distance = 0.0
    for box in boxes:
        max_dist = max(abs(box[0] - dest[0]) + abs(box[1] - dest[1]) for dest in board.destinations)
        distance += max_dist
    return distance