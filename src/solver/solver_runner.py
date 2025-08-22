from typing import Optional

from src.deadlock_detector.deadlock_detector import DeadlockDetector
from src.dto.solver_solution import SolverSolution
from src.enums.search_methods import SearchMethods
from src.model.board import Board
from src.parser.level_file_parser import LevelFileParser
from src.repository.solution_repository import SolverSolutionRepository
from src.searcher.a_star_search import AStarSearch
from src.searcher.breadth_first_search import BreadthFirstSearch
from src.searcher.depth_first_search import DepthFirstSearch


class SolverRunner:

    def __init__(self):
        self.parser = LevelFileParser()
        self.level_file = ''
        self._level_num: Optional[int] = None
        self._searcher: Optional[str] = None
        self._check_deadlocks: bool = True

    def set_level_num(self, level_num: int):
        self._level_num = level_num

    def set_searcher(self, searcher: str):
        self._searcher = searcher

    def set_level_file(self, level_file: str):
        self.level_file = level_file

    def set_check_deadlocks(self, check_deadlocks):
        self._check_deadlocks = check_deadlocks

    def get_searcher(self) -> str:
        return self._searcher

    def execute(self, board: Board) -> SolverSolution:
        if self._check_deadlocks:
            deadlock_detector = DeadlockDetector(board)
            deadlock_detector.detect_deadlocks()

        match self._searcher:
            case SearchMethods.BFS.value:
                bfs = BreadthFirstSearch(board)
                run_bench = bfs.search
            case SearchMethods.DFS.value:
                dfs = DepthFirstSearch(board)
                run_bench = dfs.search
            case SearchMethods.ASTAR.value:
                astar = AStarSearch(board)
                run_bench = astar.search
            case _:
                raise ValueError(f"Unsupported search method: {self._searcher}")

        solution: SolverSolution = run_bench()

        return solution

    def run(self, data_solution_length = None, data_solution_string = None):
        self.parser.parse(self.level_file)
        solution_repository = SolverSolutionRepository(self.get_searcher())
        board = self.parser.load_level(self.parser.level_repository.level_repository[self._level_num])

        solution = self.execute(board)
        solution_repository.__add__(solution, board.title)

        solution_repository.generate_data_csv_complete()
