# stdlib
import functools
import random

import numpy as np

from nsga2.individual import Individual


class Problem:

    def __init__(self, iproblem):
        self.bounds = iproblem.bounds
        self.dimensions = iproblem.dimensions
        self.fitness = iproblem.fitness
        self.n = len(iproblem.bounds)
        self.objectives = np.zeros((1, self.dimensions))

    def __dominates(self, individual2, individual1):
        f1 = self.fitness(individual1.features)
        f2 = self.fitness(individual2.features)

        not_dominated = all(map(lambda f: f[0] <= f[1], zip(f1, f2)))
        dominates = any(map(lambda f: f[0] < f[1], zip(f1, f2)))

        return not_dominated and dominates

    def generateIndividual(self):
        individual = Individual()
        individual.features = []
        for i in range(self.n):
            individual.features.append(random.uniform(self.bounds[i][0], self.bounds[i][1]))
        self.calculate_objectives(individual)
        individual.dominates = functools.partial(self.__dominates, individual1=individual)
        return individual

    def calculate_objectives(self, individual):
        individual.objectives = []
        individual.normalized_objectives = []

        for i, f in enumerate(self.fitness(individual.features)):
            if self.objectives.shape[0] == 1:
                self.objectives[0, i] = f
            mean = self.objectives[:, i].mean()
            std = self.objectives[:, i].std() or 1
            f_standardized = (f - mean) / std
            individual.normalized_objectives.append(f_standardized)
            individual.objectives.append(f)
        self.objectives = np.append(self.objectives, np.array([individual.objectives]), 0)
