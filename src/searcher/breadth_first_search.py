import time

from src.dto.solver_solution import SolverSolution
from src.model.board import Board


class BreadthFirstSearch:

    def __init__(self, board: Board, max_time: int):
        self._solve_board = board
        self._get_moves = self._solve_board.generate_moves_from_tuple
        self.max_time = max_time

    def search(self) -> SolverSolution | None:
        visited = []
        node = tuple(sorted(self._solve_board.boxes)), self._solve_board.player
        queue = [[node, '']]

        start_time = time.time()

        while queue:
            if time.time() - start_time > self.max_time:
                return SolverSolution(
                    False,
                    solution_string='',
                    total_steps=0,
                    push_count=0,
                    nodes_visited=len(visited),
                    processing_time=self.max_time,
                    nodes_left_in_frontier=len(queue)
                )

            node = queue.pop(0)

            if self._solve_board.is_finished_from_tuple(node[0][0]):
                end_time = time.time()
                return SolverSolution(
                    True,
                    solution_string = node[1],
                    total_steps = len(node[1]),
                    push_count = len([push for push in node[1] if push.isupper()]),
                    nodes_visited = len(visited),
                    processing_time = end_time - start_time,
                    nodes_left_in_frontier = len(queue)
                )

            if node[0] not in visited:
                visited.append(node[0])
                moves = self._get_moves(node[0][0], node[0][1])

                for move in moves:
                    new_node = self._solve_board.move_player_from_tuple(node[0][0], move)
                    queue.append([new_node, node[1] + move.str])

        return None