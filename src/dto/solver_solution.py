from dataclasses import dataclass


@dataclass
class SolverSolution:
    was_solved: bool
    solution_string: str = None
    total_steps: int = 0
    push_count: int = 0
    nodes_visited: int = None

    def __str__(self):
        return f'solved: {self.was_solved}\n' \
               f'solution: {self.solution_string}\n' \
               f'total steps: {self.total_steps}\n' \
               f'pushes: {self.push_count}\n' \
               f'nodes visited: {self.nodes_visited}'