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
from src.searcher.greedy_search import GreedySearch
from src.searcher.iterative_deepening_depth_first_search import IterativeDeepeningDepthFirstSearch


class SolverRunner:

    def __init__(self):
        self.parser = LevelFileParser()
        self.level_file = ''
        self._level_num: Optional[int] = None
        self._searcher: Optional[str] = None
        self._heuristic: Optional[str] = None
        self._check_deadlocks: bool = True
        self._limiter: int = 0
        self._max_time: int = 0

    def set_level_num(self, level_num: int):
        self._level_num = level_num

    def set_searcher(self, searcher: str):
        self._searcher = searcher

    def set_heuristic(self, heuristic: str):
        self._heuristic = heuristic

    def set_level_file(self, level_file: str):
        self.level_file = level_file

    def set_check_deadlocks(self, check_deadlocks):
        self._check_deadlocks = check_deadlocks

    def set_limiter(self, limiter: int):
        self._limiter = limiter

    def set_max_time(self, max_time: int):
        self._max_time = max_time

    def get_searcher(self) -> str:
        return self._searcher
    
    def get_heuristic(self) -> str:
        return self._heuristic

    def execute(self, board: Board) -> SolverSolution:
        if self._check_deadlocks:
            deadlock_detector = DeadlockDetector(board)
            deadlock_detector.detect_deadlocks()

        match self._searcher:
            case SearchMethods.BFS.value:
                bfs = BreadthFirstSearch(board, max_time=self._max_time)
                run_bench = bfs.search
            case SearchMethods.DFS.value:
                dfs = DepthFirstSearch(board, max_time=self._max_time)
                run_bench = dfs.search
            case SearchMethods.ASTAR.value:
                astar = AStarSearch(board, max_time=self._max_time, heuristic_type=self._heuristic)
                run_bench = astar.search
            case SearchMethods.GREEDY.value:
                greedy = GreedySearch(board, max_time=self._max_time, heuristic_type=self._heuristic)
                run_bench = greedy.search
            case SearchMethods.IDDFS.value:
                iddfs = IterativeDeepeningDepthFirstSearch(board, max_time=self._max_time, limiter=self._limiter)
                run_bench = iddfs.search
            case _:
                raise ValueError(f"Unsupported search method: {self._searcher}")

        solution: SolverSolution = run_bench()

        return solution
    
    def get_level_by_title(self, level_file: str):
        return next((level for level in self.parser.level_repository.level_repository if level.level_file == level_file), None)

    def run(self, data_solution_length = None, data_solution_string = None):
        self.parser.parse(self.level_file)
        solution_repository = SolverSolutionRepository(self.get_searcher(), self.get_heuristic())
        #board = self.parser.load_level(self.parser.level_repository.level_repository[self._level_num])
        board = self.parser.load_level(self.get_level_by_title(self.level_file))

        solution = self.execute(board)
        solution_repository.__add__(solution, board.title)

        solution_repository.generate_data_csv_complete()
