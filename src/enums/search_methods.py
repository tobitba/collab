from enum import Enum


class SearchMethods(Enum):
    BFS = 'bfs'
    DFS = 'dfs'
    GREEDY = 'greedy'
    ASTAR = 'astar'
    IDDFS = 'iddfs'