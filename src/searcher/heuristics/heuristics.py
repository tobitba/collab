import numpy as np

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