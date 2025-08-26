from typing import Optional

from src.enums.move_symbols import MoveSymbols
from src.model.move import Move


class Board:

    def __init__(self):
        self.player: Optional[tuple] = None
        self.boxes: Optional[tuple] = None
        self.destinations: Optional[tuple] = None
        self.walls: Optional[tuple] = None
        self.title = None
        self.level: Optional[tuple] = None
        self.reachable_positions: Optional[list] = None

    def print_level(self):
        for i in range(0, len(self.level)):
            print(self.level[i])
        print(self.title)
        print(" ")

    @staticmethod
    def _create_move(move: tuple[int, int, str], to_y: int, to_x: int, push: bool = False, box_y: int = None, box_x: int = None) -> Move:
        m = Move()
        m.move_to_position = (to_y, to_x)
        m.move_vector = (move[0], move[1])
        m.is_box_move = push
        m.str = move[2]

        if push:
            m.str = m.str.upper()
            m.box_to_position = (box_y, box_x)
        return m

    def generate_moves_from_tuple(self, boxes: tuple, player: tuple) -> list[Move]:
        move_vectors = [(0, -1, MoveSymbols.LEFT.value), (-1, 0, MoveSymbols.UP.value), (0, 1, MoveSymbols.RIGHT.value), (1, 0, MoveSymbols.DOWN.value)]
        moves = []
        for move in move_vectors:
            new_player_pos = player[0] + move[0], player[1] + move[1]
            if new_player_pos in boxes:  # box push
                new_box_pos = new_player_pos[0] + move[0], new_player_pos[1] + move[1]
                if new_player_pos not in self.walls and new_box_pos not in boxes  and new_box_pos not in self.walls:  # legal push
                    if self.reachable_positions is None or new_box_pos in self.reachable_positions:
                        moves.append(self._create_move(
                            move,
                            new_player_pos[0],
                            new_player_pos[1],
                            push = True,
                            box_x=new_box_pos[1],
                            box_y = new_box_pos[0]
                        ))
            else:
                if new_player_pos not in self.walls:
                    moves.append(self._create_move(
                        move,
                        new_player_pos[0],
                        new_player_pos[1]
                    ))

        return moves

    def is_finished_from_tuple(self, boxes: tuple) -> bool:
        return sorted(boxes) == sorted(self.destinations)

    @staticmethod
    def move_player_from_tuple(boxes: tuple, move: Move):
        player = move.move_to_position
        if move.is_box_move:
            boxes = list(boxes)
            boxes.remove(move.move_to_position)
            boxes.append(move.box_to_position)
            boxes = tuple(boxes)
        return tuple(sorted(boxes)), player