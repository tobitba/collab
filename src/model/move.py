from typing import Optional


class Move:

    def __init__(self):
        self.str: str = ""
        self.move_vector: tuple[int, int] = (0, 0)
        self.move_to_position: tuple[int, int] = (0, 0)
        self.box_to_position: Optional[tuple[int, int]] = None
        self.is_box_move: bool = False