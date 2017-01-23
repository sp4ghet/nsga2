import csv
import numpy as np
from deap import benchmarks


dimensions = 3
bounds = np.array([[0, 1] for _ in range(dimensions)])


def fitness(x):
    return benchmarks.dtlz1(x, dimensions)

# TODO: use np.fromiter instead of np.array on list comprehension
def perfect_pareto_front():
    with open('./DTLZ1_pf.csv', encoding='utf8') as file:
        p = [list(map(float, row)) for row in csv.reader(file)]
        return np.array(p)
