from operator import attrgetter
from population import Population
from instance import Instance
import random
import copy


class GeneticAlgorithm:

    # GERA POPULAÇÃO INICIAL
    def generate_population(self, path, n):
        pop = Population()
        pop.generate_population(n, path)
        return pop.get_instances()

    # CALCULA A FUNÇÃO FITNESS DE UM INDIVÍDUO (LINEAR RANKING)

    def fitness(self, population, SP):
        fitness = []
        Nind = len(population)
        population.sort(key=attrgetter('distance'), reverse=True)
        for i in range(len(population)):
            fitness.append(2 - SP + 2 * (SP - 1) * (i / (Nind - 1)))
            population[i].set_fitness(fitness[i])
        population.reverse()
        fitness.sort(reverse=True)
        # for i in population:
        #     print(i.get_distance(), i.get_fitness())
        # print()
        return fitness

    # VERIFICA SE EXISTEM INSTANCIAS REPETIDAS NA LISTA
    def repeated(self, arr):
        a = b = 0
        for i in range(len(arr)):
            a = arr[i].get_distance()
            for j in range(len(arr)):
                b = arr[j].get_distance()
                if a == b and j != i:
                    return 1
        return 0

    # SELECIONA INDIVÍDUOS POR MEIO DO FITNESS E PROBABILIDADE
    # NÃO ESTOU USANDO NO MOMENTO
    def roulette_wheel_selection(self, fitness, population):
        prob = []
        num = []
        selected = []
        soma = flag = 0
        sum_fitness = sum(fitness)
        for i in range(len(fitness)):
            prob.append(fitness[i] / sum_fitness)

        for i in range(len(prob)):
            soma += prob[i]
            prob[i] = soma

        # SELECIONA DUAS INSTÂNCIAS DIFERENTES COM BASE NA PROBABILIDADE
        while True:
            for i in range(2):
                num.append(random.uniform(0, 1))

            for i in range(len(num)):
                for j in range(len(prob)):
                    if num[i] <= prob[j]:
                        selected.append(copy.deepcopy(population[j]))
                        break
            flag = self.repeated(selected)
            if flag == 0:
                break
            else:
                num.clear()
                selected.clear()
        return selected

    # UTILIZA TOUNAMENT SELECTION PARA DEFINIR OS PAIS (ESTOU USANDO ESSA)
    def parents_selection(self, population, k):
        parents = []
        pop = copy.deepcopy(population)
        k = round(k * len(population))
        for i in range(2):
            parents.append(self.tournament_selection(pop, k))
        return parents

    # RETORNA A SEQUÊNCIA DE VISITAÇÃO DE UMA INSTÂNCIA
    def visiting_sequence(self, list, cut_points, inherited):
        seq = []
        i = cut_points[1]
        while True:
            seq.append(list[i].get_id())
            i += 1
            if i == len(list):
                i = 0
            if i == cut_points[1]:
                break
        for i in inherited:
            seq.remove(i)
        return seq

    # RECEBE UM ID E RETORNA O CLIENTE CORRESPONDENTE
    def get_client(self, id, list):
        for i in list:
            if i.get_id() == id:
                return i
        return 0

    # CRIA OS DESCENDENTES
    def offspring(self, p1, p2, cut_points):
        q = []
        # INICIALIZA O FILHO COM UM CARACTERE QUALQUER (A)
        for i in range(len(p1)):
            q.append('A')
        inherited = []
        # COPIA A PARTE HERDADA DO PAI PARA O FILHO
        for i in range(cut_points[0], cut_points[1]):
            q[i] = p1[i]
            inherited.append(p1[i].get_id())
        # SEQ RECEBE A SEQUENCIA DE VISITAÇÃO DE P2
        seq = self.visiting_sequence(p2, cut_points, inherited)
        i = cut_points[1]
        k = 0
        # COPIA OS ELEMENTOS DA LISTA CONTENDO A SEQUENCIA DE P2 EM F1
        while True:
            if seq[k] in inherited:
                k += 1
            q[i] = self.get_client(seq[k], p1)
            i += 1
            k += 1
            if k == len(seq) or i == cut_points[0]:
                break
            if i == len(p1):
                i = 0
        return q

    # É NECESSÁRIO INFORMAR A QUANTIDADE DE CLIENTES (ATENÇÃO A COMO OS PONTOS DE CORTE SÃO ESCOLHIDOS)
    # NO CASO ESTOU CONSIDERANDO QUE OS PONTOS DE CORTE COMEÇAM DE 2 ATE N-2, O QUE ME DEIXA COM UAM MARGEM MINIMA NA DIVISÃO DA LISTA

    # ORDER COSSOVER OPERATION // ESPEFIFICAR Ã QUANTIDADE DE CLIENTES = n
    # O PRIMEIRO PONTO DE CORTE SO PODE SER NO MÁXIMO IGUAL AO NÚMERO DE CLIENTES - 2
    # PARA GARANTIR QUE EXISTAM 3 DIVISÕES 
    def crossover(self, n, parents):
        cut_points = []
        cut_points.append(random.randint(1, n - 2))
        cut_points.append(random.randint(cut_points[0] + 1, n - 1))

        offsprings = []
        p1 = parents[0].get_all_clients()
        p2 = parents[1].get_all_clients()

        off1 = self.offspring(p1, p2, cut_points)
        off2 = self.offspring(p2, p1, cut_points)

        offsprings.append(self.new_instance(parents[0], off1))
        offsprings.append(self.new_instance(parents[0], off2))
        return offsprings

    # RECEBE UMA LISTA DE CLIENTES COMO PARAMETRO E RETORNA UMA INSTANCIA

    def new_instance(self, instance, clientList):
        new_instance = Instance()
        new_instance.set_clientList(clientList)
        new_instance.set_adjMatrix(instance.get_adjMatrix())
        new_instance.set_capacity(instance.get_capacity())
        new_instance.initial_solution()
        return new_instance

   	# UMA PROBABILIDADE DE 20% FOI ESTIPULADA PARA A REALIZAÇÃO
    # SWAP MUTATION

    def mutation(self, s):
        while True:
            i = random.randint(0, len(s.get_vehicleList()) - 1)
            vehicle = s.get_vehicleList()[i]
            if len(vehicle.get_route()) > 3:
                break
        # ID = 0 SIGNIFICA DEPÓSITO 
        while True:
            vehicle_c = copy.deepcopy(vehicle)
            while True:
                c1, c2 = random.sample(vehicle.get_route(), 2)
                if c1.get_id() != 0 and c2.get_id() != 0:
                    break
            c1_index = vehicle.get_index(c1) 
            c2_index = vehicle.get_index(c2)
            vehicle_c.remove_client(c1)
            vehicle_c.remove_client(c2)
            vehicle_c.insert_client(c1_index, c2)
            vehicle_c.insert_client(c2_index, c1)           
            s.create_temp_route(vehicle_c)
            a = vehicle_c.is_feasible()
            if a == 1:
                s.remove_vehicle(vehicle)
                s.add_vehicle(vehicle_c)
                s.update_distance()
                break
        return s



    # A POPULAÇÃO DEVE TER UM TAMANHO MÍNIMO DE 20
    # PARA A SELEÇÃO DE SOVREVIVENTES SER FEITA CORRETAMENTE
    def survivor_selection(self, population, candidates):
        survivors = []
        temporary_pop = candidates[:]
        k = 0
        n = 0
        # ELITISMO = 5%
        n = round(len(population) * 0.05)
        for i in range(n):
            survivors.append(temporary_pop[i])
            temporary_pop.pop(i)

        # TORNEIO = 45% K = 10% DA POPULAÇÃO // K MUITO GRANDE PODE GERAR ELITISMO ?
        n = round(len(population) * 0.45)
        k = round(0.1 * len(population))
        for i in range(n):
            survivors.append(self.tournament_selection(temporary_pop, k))

        # ESCOLHA ALEATÓRIA 55%, PODE SER MAIS DEPENDENDO DO TAMANHO DA POPULAÇAO
        while True:
            if len(survivors) == len(population):
                break
            survivors.append(
                temporary_pop[random.randint(0, len(temporary_pop) - 1)])
            temporary_pop.remove(survivors[-1])

        # print('inicial pop')
        # for i in population:
        # 	print(i.get_distance())
        # print('sec pop')
        # for i in survivors:
        # 	print(i.get_distance())


    # REALIZA UM TORNEIRO ENTRE % DA POPULAÇÃO
    def tournament_selection(self, population, k):
        selected = []
        random_num = []
        random_num = list(
            map(int, random.sample(range(0, len(population)), k)))
        for i in random_num:
            selected.append(population[i])
        selected.sort(key=attrgetter('fitness'), reverse=True)
        population.remove(selected[0])
        return selected[0]
