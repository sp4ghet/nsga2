"""NSGA-II related functions"""

import functools
import random

import numpy as np

from nsga2.population import Population


class NSGA2Utils(object):
    
    def __init__(self, problem, num_of_individuals, mutation_strength=0.2, num_of_genes_to_mutate=5, num_of_tour_particips=2):
        
        self.problem = problem
        self.num_of_individuals = num_of_individuals
        self.mutation_strength = mutation_strength
        self.number_of_genes_to_mutate = min(num_of_genes_to_mutate, problem.n - 1)
        self.num_of_tour_particips = num_of_tour_particips
        
    def fast_nondominated_sort(self, population):
        """
        Conduct nondominated_sort on population(Iterable of nsga2.individual.Individual)
        Section 3.1 (p.4) on paper.

        :param population:
        :type population: nsga2.population.Population

        :return: None

        .. warning:: population is modified and nondominated_sort is applied.
        """
        population.fronts = []
        population.fronts.append([])

        for individual in population:
            individual.domination_count = 0
            individual.dominated_solutions = set()

            for other_individual in population:
                if individual.dominates(other_individual):
                    individual.dominated_solutions.add(other_individual)
                elif other_individual.dominates(individual):
                    individual.domination_count += 1
            if individual.domination_count == 0:
                population.fronts[0].append(individual)
                individual.rank = 0
        i = 0
        while len(population.fronts[i]) > 0:
            temp = []
            for individual in population.fronts[i]:
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i+1
                        temp.append(other_individual)
            i = i+1
            population.fronts.append(temp)

    def calculate_crowding_distance(self, front):
        if len(front) > 0:
            for individual in front:
                individual.crowding_distance = 0

            for m in range(len(front[0].normalized_objectives)):
                front = sorted(front, key=lambda x: x.normalized_objectives[m])
                front[0].crowding_distance = float('inf')
                front[-1].crowding_distance = float('inf')
                for index, value in enumerate(front[1:-1]):
                    index += 1
                    front[index].crowding_distance += (front[index + 1].normalized_objectives[m] - front[index - 1].normalized_objectives[m])

    def crowding_operator(self, individual, other_individual):
        less_crowded = (individual.crowding_distance > other_individual.crowding_distance)
        if (individual.rank < other_individual.rank) or ((individual.rank == other_individual.rank) and less_crowded):
            return 1
        else:
            return -1
    
    def create_initial_population(self):
        population = Population()
        for _ in range(self.num_of_individuals):
            individual = self.problem.generateIndividual()
            self.problem.calculate_objectives(individual)
            population.population.append(individual)
            
        return population
    
    def create_children(self, population):
        children = []
        self.problem.objectives = np.ones((1, self.problem.dimensions))
        while len(children) < len(population):
            parent1 = self.__tournament(population)
            parent2 = parent1
            while parent1.features == parent2.features:
                parent2 = self.__tournament(population)
            child1, child2 = self.__crossover(parent1, parent2)
            self.__mutate(child1)
            self.__mutate(child2)
            self.problem.calculate_objectives(child1)
            self.problem.calculate_objectives(child2)
            children.append(child1)
            children.append(child2)

        return children
    
    def __crossover(self, individual1, individual2):
        child1 = self.problem.generateIndividual()
        child2 = self.problem.generateIndividual()
        genes_indexes = range(len(child1.features))
        half_genes_indexes = random.sample(genes_indexes, 1)
        for i in genes_indexes:
            if i in half_genes_indexes:
                child1.features[i] = individual2.features[i]
                child2.features[i] = individual1.features[i]
            else:
                child1.features[i] = individual1.features[i]
                child2.features[i] = individual2.features[i]
        return child1, child2

    def __mutate(self, child):
        genes_to_mutate = random.sample(range(0, len(child.features)), self.number_of_genes_to_mutate)
        for gene in genes_to_mutate:
            child.features[gene] += random.random() * self.mutation_strength - self.mutation_strength/2
            if child.features[gene] < self.problem.bounds[gene][0]:
                child.features[gene] = self.problem.bounds[gene][0]
            elif child.features[gene] > self.problem.bounds[gene][1]:
                child.features[gene] = self.problem.bounds[gene][1]
        
    def __tournament(self, population):
        """

        :param population: ioptimizer.nsga2.population.Population
        :return:
        """
        participants = random.sample(population.population, self.num_of_tour_particips)
        return max(sorted(participants,
                          key=functools.cmp_to_key(self.crowding_operator)),
                   key=functools.cmp_to_key(self.crowding_operator))
