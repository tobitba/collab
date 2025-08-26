from typing import Optional


class Level:

    def __init__(self):
        self.array: Optional[list] = None
        self.title: Optional[str] = None
        self.level_file: Optional[str] = None
        self.level_id: Optional[int] = None