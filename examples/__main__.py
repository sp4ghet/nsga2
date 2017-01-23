from examples import *
import examples.dtlz1 as dtlz1
import nsga2

def multiobjective_benchmark(optimizer, problem):
    """

    :param optimizer: IOptimizer
    :param problem: IProblem
    :return: None
    """

    epochs = 100
    agents_number = 100

    p = problem.perfect_pareto_front()
    for i, result in enumerate(optimizer(problem, epochs, agents_number)):
        print('Epoch %i' % i)
        hv = hypervolume(result[1], [11 for _ in range(problem.dimensions)])
        phv = hypervolume(p, [11 for _ in range(problem.dimensions)])
        print('current hypervolume: ', hv)
        print('maximum hypervolume: ', phv)
        print('HVR: ', hv / phv)
        if i % 20 == 0:
            c = convergence(result[1], p)
            print('convergence: ', c)
            draw_pareto(i, result, p, dim=problem.dimensions)


multiobjective_benchmark(nsga2.call, dtlz1)

input()
