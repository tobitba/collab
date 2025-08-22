import time

from src.dto.solver_solution import SolverSolution
from src.model.board import Board


class BreadthFirstSearch:

    def __init__(self, board: Board):
        self._solve_board = board
        self.__start_time: float = time.time()
        self.max_time: int = 300  # Maximum time in seconds to run the search
        self._get_moves = self._solve_board.generate_moves_from_tuple

    def search(self) -> SolverSolution | None:
        visited = []
        node = tuple(sorted(self._solve_board.boxes)), self._solve_board.player
        queue = [[node, '']]

        while queue:
            node = queue.pop(0)

            if self._solve_board.is_finished_from_tuple(node[0][0]):
                return SolverSolution(
                    True,
                    solution_string = node[1],
                    total_steps = len(node[1]),
                    push_count = len([push for push in node[1] if push.isupper()]),
                    nodes_visited = len(visited)
                )

            if node[0] not in visited:
                visited.append(node[0])
                moves = self._get_moves(node[0][0], node[0][1])

                for move in moves:
                    new_node = self._solve_board.move_player_from_tuple(node[0][0], move)
                    queue.append([new_node, node[1] + move.str])
        return None