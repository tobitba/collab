import argparse
import glob
import re

from src.solver.solver_runner import SolverRunner
from src.enums.search_methods import SearchMethods

def plot_results():
    from src.repository.plot_repository import plot
    plot()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Sokoban solution search")
    parser.add_argument("--algorithm", default="all", help="Selected algorithm for searcher (bfs, dfs, astar, greedy, iddfs, all)")
    parser.add_argument("--heuristic", default="all", help="Heuristic to use (manhattan, wall_aware, max_distance, all)")
    parser.add_argument("--maxTime", type=int, default=300, help="Max time for searcher to run")
    parser.add_argument("--limiter", type=int, default=100000, help="Limit for IDDFS")
    parser.add_argument("--checkDeadlocks", type=bool, default=True, help="Check deadlock before search starts")
    parser.add_argument("--level", type=int, default=0, help="Sokoban level number (0 = all levels)")
    parser.add_argument("--plot", type=bool, default=True, help="Run plot analysis afterwards")
    args = parser.parse_args()
    runner = SolverRunner()
    levels = []

    heuristic_options = ["manhattan", "wall_aware", "max_distance"]

    if args.algorithm.lower() == "all":
        algorithms = [SearchMethods.BFS.value, SearchMethods.DFS.value, SearchMethods.ASTAR.value, SearchMethods.GREEDY.value, SearchMethods.IDDFS.value]
    else:
        algorithms = [args.algorithm.lower()]

    if args.level == 0:
        level_files = sorted(glob.glob("data/soko*.txt"))
        
        for file in level_files:
            match = re.search(r"soko(\d+)\.txt", file)
            if match:
                levels.append((int(match.group(1)), file) )
    else:
        levels = [(args.level, f"data/soko{args.level}.txt")]
        
    for idx, (level_num, level_file) in enumerate(levels):
        runner.set_level_file(level_file)
        runner.set_level_num(idx)

        for algorithm in algorithms:
            runner.set_searcher(algorithm)
            runner.set_check_deadlocks(args.checkDeadlocks)
            runner.set_limiter(args.limiter)
            runner.set_max_time(args.maxTime)

            if args.heuristic.lower() == "all" and algorithm in [SearchMethods.ASTAR.value, SearchMethods.GREEDY.value]:
                for heuristic in heuristic_options:
                    runner.set_heuristic(heuristic)
                    runner.run()
            else:
                runner.set_heuristic(args.heuristic.lower())
                runner.run()

    if args.plot:
        plot_results()