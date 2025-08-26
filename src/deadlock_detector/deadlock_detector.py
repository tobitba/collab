from src.enums.move_symbols import MoveSymbols
from src.model.board import Board


class DeadlockDetector:

    def __init__(self, board: Board):
        self.board = board
        self.reachable_positions = []

    def detect_deadlocks(self):
        reachable_positions = []

        for destination in self.board.destinations:
            reachable_positions.append(destination)

            node = destination
            visited = []
            queue = [node]

            while queue:
                node = queue.pop(0)
                pull_positions = self._generate_reachable_positions_by_pull(node)

                for position in pull_positions:
                    if position not in visited:
                        visited.append(position)
                        queue.append(position)
                        reachable_positions.append(position)

        self.reachable_positions = sorted(list(dict.fromkeys(reachable_positions)))
        self.board.reachable_positions = self.reachable_positions

    def _generate_reachable_positions_by_pull(self, destination: tuple[int, int]):
        move_vectors = [(0, -1, MoveSymbols.LEFT.value), (-1, 0, MoveSymbols.UP.value), (0, 1, MoveSymbols.RIGHT.value), (1, 0, MoveSymbols.DOWN.value)]
        reachable_positions = []
        box_pos = destination

        for move in move_vectors:
            new_box_pos = box_pos[0] + move[0], box_pos[1] + move[1]
            new_player_pos = new_box_pos[0] + move[0], new_box_pos[1] + move[1]

            if new_player_pos not in self.board.walls and new_box_pos not in self.board.walls:
                reachable_positions.append(new_box_pos)

        return reachable_positions