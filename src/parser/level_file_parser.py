import logging

from src.enums.board_symbols import BoardSymbols
from src.model.board import Board
from src.model.level import Level
from src.repository.level_repository import LevelRepository


class LevelFileParser:

    def __init__(self):
        self.level_file = None
        self.file_path = None
        self.level_repository: LevelRepository = LevelRepository()

    def parse(self, level_file: str):
        self.level_file = level_file
        self.file_path = level_file
        file = open(self.file_path, "r")

        level = []
        level_class = Level()
        level_id = 0
        single_line = []

        for line in file:
            if line.find('Title') >= 0:
                level_class.title = line[:-1]
            elif line.find('\n') >= 0 > line.find('#'):
                level_class.level_file = self.level_file
                level_class.level_id = level_id
                level_class.array = level

                level_id += 1
                level = []

                self.level_repository.level_repository.append(level_class)
                level_class = Level()
            else:
                for char in line:
                    if char == '':
                        single_line.append(' ')
                    else:
                        single_line.append(char)
                level.append(list(line[:-1]))
                single_line = []

        file.close()
        logging.log(logging.INFO, "Imported level file")

    @staticmethod
    def load_level(level: Level) -> Board:
        level_array = level.array
        player = []
        boxes = []
        destinations = []
        walls = []

        for i in range(0, len(level_array)):
            for j in range(0, len(level_array[i])):
                if level_array[i][j] == BoardSymbols.PLAYER.value:
                    player = (i, j)
                if level_array[i][j] == BoardSymbols.PLAYER_ON_STORAGE.value:
                    player = (i, j)
                    destinations.append((i, j))
                if level_array[i][j] == BoardSymbols.BOX.value:
                    boxes.append((i, j))
                if level_array[i][j] == BoardSymbols.BOX_ON_STORAGE.value:
                    boxes.append((i, j))
                    destinations.append((i, j))
                if level_array[i][j] == BoardSymbols.STORAGE.value:
                    destinations.append((i, j))
                if level_array[i][j] == BoardSymbols.WALL.value:
                    walls.append((i, j))

        board = Board()

        board.player = tuple(player)
        board.boxes = tuple(boxes)
        board.destinations = tuple(destinations)
        board.walls = tuple(walls)

        board.title = level.title
        board.level = level_array

        return board