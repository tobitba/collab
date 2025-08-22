from queue import PriorityQueue

from src.dto.prioritized_node import PrioritizedNode
from src.dto.solver_solution import SolverSolution
from src.model.board import Board
from src.model.move import Move
from src.searcher.heuristics.heuristics import manhattan_distance


class AStarSearch:

    def __init__(self, board: Board):
        self.board: Board = board
        self._get_moves = self.board.generate_moves_from_tuple

    def _get_static_weighting(self, boxes: tuple):
        return manhattan_distance(self.board, boxes) * 2.2

    def _get_heuristic_value(self, boxes: tuple, move: Move) -> float:
        return self._get_static_weighting(boxes)

    def search(self) -> SolverSolution | None:
        open_list = PriorityQueue()
        open_list_lookup = {}
        closed_list_lookup = {}

        item = tuple(sorted(self.board.boxes)), self.board.player
        node: PrioritizedNode = PrioritizedNode(
            priority = 0,
            item = item,
            action = ''
        )

        open_list.put(node)
        open_list_lookup.update({node.item: 0})

        while open_list:
            q: PrioritizedNode = open_list.get()  # q.item[0] = boxes and q.item[1] = player
            open_list_lookup.pop(q.item, None)

            if self.board.is_finished_from_tuple(q.item[0]):
                return SolverSolution(
                    True,
                    solution_string = q.action,
                    total_steps = len(q.action),
                    push_count = len([push for push in q.action if push.isupper()]),
                    nodes_visited = len(closed_list_lookup)
                )

            moves = self._get_moves(q.item[0], q.item[1])

            for move in moves:
                new_node = self.board.move_player_from_tuple(q.item[0], move)
                heuristic = self._get_heuristic_value(new_node[0], move)
                cost = len(q.action) + len(move.str)

                open_list_node_priority = open_list_lookup.get(new_node)
                closed_list_node_priority = closed_list_lookup.get(new_node)

                if open_list_node_priority is not None and open_list_node_priority < cost + heuristic:
                    continue

                if closed_list_node_priority is not None and closed_list_node_priority < cost + heuristic:
                    continue

                add_node = PrioritizedNode(
                    priority = cost + heuristic,
                    item = new_node,
                    action = q.action + move.str
                )
                open_list.put(add_node)
                open_list_lookup.update({new_node: cost + heuristic})

            closed_list_lookup.update({q.item: q.priority})

        return None