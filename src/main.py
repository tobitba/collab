import argparse

from src.solver.solver_runner import SolverRunner

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Sokoban solution search")
    parser.add_argument("--algorithm", default="bfs", help="Selected algorithm for searcher (BFS,DFS,AStar)")
    parser.add_argument("--maxTime", type=int, help="Max time for searcher to run")
    parser.add_argument("--limiter", type=int, help="Limit for DFS") #not implemented
    parser.add_argument("--checkDeadlocks", type=bool, default=True , help="Check deadlock before search starts")
    parser.add_argument("--level", default=1, help="Sokoban level number")
    args = parser.parse_args()
    runner = SolverRunner()

    runner.set_level_file('data/soko{level}.txt'.format(level=args.level))
    runner.set_level_num(0)
    runner.set_searcher(args.algorithm)
    runner.set_check_deadlocks(args.checkDeadlocks)
    runner.run()