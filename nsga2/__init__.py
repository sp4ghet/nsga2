from nsga2.interfaces.ioptimizer import *

from nsga2.evolution import Evolution
from nsga2.problem import Problem


def seq(start, stop, step=1):
    n = int(round((stop - start)/float(step)))
    if n > 1:
        return([start + step*i for i in range(n+1)])
    else:
        return([])


def call(iproblem: IProblem, epochs: int, agent_count: int) -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
    yield from NSGA2.call(iproblem, epochs, agent_count)


class NSGA2(IOptimizer):

    @staticmethod
    def call(iproblem: IProblem, epochs: int, agent_count: int) -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
        problem = Problem(iproblem)
        evolution = Evolution(problem, epochs, agent_count)
        for pop in evolution.evolve():
            xs = [x for x in map(lambda x: x.features, pop.fronts[0])]
            fs = [f for f in map(lambda x: x.objectives, pop.fronts[0])]
            # f_norms = [x for x in map(lambda x: x.normalized_objectives, pop.fronts[0])] # Originally here for debugging purposes
            yield np.array(xs), np.array(fs)