from genetic_algorithm import GeneticAlgorithm
from local_search import LS
from population import Population
import random
import copy
import time

filhos = []
algo = GeneticAlgorithm()

inicio = time.time()
n = 0
# for i in range(1):
# 	f = algo.fitness(pop, 1.7)
# # selected = algo.roulette_wheel_selection(f, pop)
# 	parents = algo.parents_selection(pop, 0.1)
# 	algo.crossover(50, parents)
# filhos = pop[:]
# filhos.extend(algo.crossover(50, selected))
# filhos.extend(algo.crossover(50, selected))
# algo.fitness(filhos, 1.7)
# algo.survivor_selection(pop, filhos)
ls = LS()
s = ls.local_search(pop[0], 50)
# algo.mutation(pop[0])
# ils.two_opt_01(pop[0])

# fim = time.time()
# print(fim - inicio)
#IMPLEMENTAR MUTAÇÃO
