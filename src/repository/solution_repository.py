import os
import pandas as pd
import logging

from src.dto.solver_solution import SolverSolution


class SolverSolutionRepository:

    def __init__(self, solver: str, heuristic: str):
        self.__solver = solver
        self.__heuristic = heuristic
        self.__solver_solutions: list[SolverSolution] = []
        self.__level_titles: list = []
        self.__show_header: bool = True

    def __add__(self, solution: SolverSolution, level_title: str):
        self.__solver_solutions.append(solution)
        self.__level_titles.append(level_title)

    def generate_data_csv_complete(self):
        os.makedirs('results', exist_ok=True)

        run_number = []
        solved = []
        total_steps = []
        push_moves = []
        nodes_visited = []
        solution_string = []
        processing_time = []
        nodes_left_in_frontier = []

        for i in range(0, len(self.__solver_solutions)):
            run_number.append(i)
            solved.append(int(self.__solver_solutions[i].was_solved))
            total_steps.append(self.__solver_solutions[i].total_steps)
            push_moves.append(self.__solver_solutions[i].push_count)
            nodes_visited.append(self.__solver_solutions[i].nodes_visited)
            solution_string.append(self.__solver_solutions[i].solution_string)
            processing_time.append(round(self.__solver_solutions[i].processing_time, 4))
            nodes_left_in_frontier.append(self.__solver_solutions[i].nodes_left_in_frontier)

        csv_format = {
            'title': self.__level_titles,
            'solved': solved,
            'total_steps': total_steps,
            'pushes': push_moves,
            'nodes_visited': nodes_visited,
            'nodes_left_in_frontier': nodes_left_in_frontier,
            'processing_time_seconds': processing_time,
            'solution_string': solution_string,
        }

        data_frame = pd.DataFrame(csv_format)

        if self.__solver == "astar" or self.__solver == "greedy":
            csv_name = f'results/{self.__solver}_{self.__heuristic}.csv'
        else:
            csv_name = f'results/{self.__solver}.csv'

        logging.log(logging.INFO, f"Writing Solutions to: {csv_name}")
        
        if os.path.exists(csv_name):
            data_frame.to_csv(csv_name, sep=';', index=False, mode='a', header=False)
        else:
            data_frame.to_csv(csv_name, sep=';', index=False, chunksize=10, header=self.__show_header)

        