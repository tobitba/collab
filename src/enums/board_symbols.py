from enum import Enum


class BoardSymbols(Enum):
    EMPTY = ' '
    WALL = '#'
    BOX = '$'
    PLAYER = '@'
    STORAGE = '.'
    PLAYER_ON_STORAGE = '+'
    BOX_ON_STORAGE = '*'