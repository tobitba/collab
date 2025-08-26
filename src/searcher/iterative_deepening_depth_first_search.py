from collections import deque
import time

from src.dto.solver_solution import SolverSolution
from src.model.board import Board


class IterativeDeepeningDepthFirstSearch:
    def __init__(self, board: Board, max_time: int, limiter: int):
        self._solve_board = board
        self._get_moves = self._solve_board.generate_moves_from_tuple
        self.max_time = max_time
        self.limiter = limiter

    def depth_limited_search(self, node, depth_limit, start_time):
        frontier = deque()
        frontier.appendleft([node, '', 0])  # node, solution_string, depth
        visited_local = set()

        while frontier:
            if time.time() - start_time > self.max_time:
                return None, len(visited_local), len(frontier), True

            current, path, depth = frontier.popleft()

            if self._solve_board.is_finished_from_tuple(current[0]):
                return path, len(visited_local), len(frontier), False

            if current not in visited_local and depth <= depth_limit:
                visited_local.add(current)

                moves = self._get_moves(current[0], current[1])
                for move in moves:
                    new_node = self._solve_board.move_player_from_tuple(current[0], move)
                    frontier.appendleft([new_node, path + move.str, depth + 1])

        return None, len(visited_local), len(frontier), False

    def search(self) -> SolverSolution | None:
        start_time = time.time()
        node = tuple(sorted(self._solve_board.boxes)), self._solve_board.player
        total_nodes_visited = 0
        timeout_occurred = False

        for depth_limit in range(self.limiter):
            if time.time() - start_time > self.max_time:
                timeout_occurred = True
                break

            solution, nodes_visited, nodes_left, timeout = self.depth_limited_search(node, depth_limit, start_time)
            total_nodes_visited += nodes_visited

            if solution is not None:
                end_time = time.time()
                return SolverSolution(
                    True,
                    solution_string=solution,
                    total_steps=len(solution),
                    push_count=len([push for push in solution if push.isupper()]),
                    nodes_visited=total_nodes_visited,
                    processing_time=end_time - start_time,
                    nodes_left_in_frontier=nodes_left
                )

            if timeout:
                timeout_occurred = True
                break

        end_time = time.time()
        process_time = self.max_time if timeout_occurred else (end_time - start_time)

        return SolverSolution(
            False,
            solution_string='',
            total_steps=0,
            push_count=0,
            nodes_visited=total_nodes_visited,
            processing_time=process_time,
            nodes_left_in_frontier=0
        )