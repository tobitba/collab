from queue import PriorityQueue
import time

from src.enums.heuristics import Heuristics
from src.dto.prioritized_node import PrioritizedNode
from src.dto.solver_solution import SolverSolution
from src.model.board import Board
from src.model.move import Move
from src.searcher.heuristics.heuristics import manhattan_distance, wall_aware_manhattan_distance, max_distance


class GreedySearch:

    def __init__(self, board: Board, max_time: int, heuristic_type: str):
        self.board: Board = board
        self._get_moves = self.board.generate_moves_from_tuple
        self.max_time = max_time
        self.heuristic_type = heuristic_type

    def _get_static_weighting(self, boxes: tuple):
        match self.heuristic_type:
            case Heuristics.MANHATTAN.value:
                return manhattan_distance(self.board, boxes)
            case Heuristics.WALL_AWARE.value:
                return wall_aware_manhattan_distance(self.board, boxes)
            case Heuristics.MAX_DISTANCE.value:
                return max_distance(self.board, boxes)

    def _get_heuristic_value(self, boxes: tuple, move: Move) -> float:
        return self._get_static_weighting(boxes)

    def search(self) -> SolverSolution | None:
        open_list = PriorityQueue()
        closed_list_lookup = {}

        item = tuple(sorted(self.board.boxes)), self.board.player
        node: PrioritizedNode = PrioritizedNode(
            priority = self._get_heuristic_value(item[0], None),
            item = item,
            action = ''
        )

        open_list.put(node)

        start_time = time.time()

        while open_list:
            if time.time() - start_time > self.max_time:
                return SolverSolution(
                    False,
                    solution_string="",
                    total_steps=0,
                    push_count=0,
                    nodes_visited=len(closed_list_lookup),
                    processing_time=self.max_time,
                    nodes_left_in_frontier=open_list.qsize()
                )

            q: PrioritizedNode = open_list.get()

            if self.board.is_finished_from_tuple(q.item[0]):
                end_time = time.time()
                return SolverSolution(
                    True,
                    solution_string = q.action,
                    total_steps = len(q.action),
                    push_count = len([push for push in q.action if push.isupper()]),
                    nodes_visited = len(closed_list_lookup),
                    processing_time = end_time - start_time,
                    nodes_left_in_frontier = open_list.qsize()
                )

            moves = self._get_moves(q.item[0], q.item[1])

            for move in moves:
                new_node = self.board.move_player_from_tuple(q.item[0], move)
                heuristic = self._get_heuristic_value(new_node[0], move)

                if new_node in closed_list_lookup:
                    continue

                add_node = PrioritizedNode(
                    priority = heuristic,
                    item = new_node,
                    action = q.action + move.str
                )
                open_list.put(add_node)

            closed_list_lookup.update({q.item: q.priority})

        return None