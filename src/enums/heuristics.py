from enum import Enum


class Heuristics(Enum):
    MANHATTAN = 'manhattan'
    WALL_AWARE = 'wall_aware'
    MAX_DISTANCE = 'max_distance'