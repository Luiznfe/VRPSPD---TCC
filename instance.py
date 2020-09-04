from vehicle import Vehicle
from data_entry import data_read
from client import Client
import random
import copy

class Instance:

    def __init__(self):
        self.id = id
        self.vehicleList = list()
        self.clientList = list()
        self.adjMatrix = list()
        self.capacity = 0.0  # CAPACIDADE DA FROTA
        self.distance = 0.0  # DISTANCIA TOTAL PERCORRIDA
        self.fitness = 0.0

    def __repr__(self):
        return str(self.id)

    def set_distance(self, distance):
        self.distance = distance

    def get_distance(self):
        return self.distance

    def set_fitness(self, fitness):
        self.fitness = fitness

    def set_id(self, id):
        self.id = id

    def set_vehicleList(self, vehicle):
        self.vehicleList.clear()
        self.vehicleList = vehicle[:]

    def set_clientList(self, client):
        self.clientList.clear()
        self.clientList = client[:]

    def set_capacity(self, cap):
        self.capacity = cap

    def set_adjMatrix(self, matrix):
        self.adjMatrix = matrix[:]

    def get_vehicleList(self):
        return self.vehicleList[:]

    def get_id(self):
        return self.id

    def get_clientList(self):
        return self.clientList[:]

    def get_adjMatrix(self):
        return self.adjMatrix[:]

    def get_capacity(self):
        return self.capacity

    def get_fitness(self):
        return self.fitness

    # LIMPA A LISTA DE VEICULOS
    def clear_vehicle_list(self):
        self.vehicleList.clear()

    # INICIA A INSTÂNCIA COM OS DADOS RECEBIDOS
    def set_instance(self, path):
        data = data_read(path)
        self.capacity = data[0]
        self.adjMatrix = data[1][:]
        self.clientList = data[2][:]

    # SOMA A DISTANCIA PERCORRIDA POR UM VEÍCULO AO TOTAL

    def sum_distance_instance(self, distance):
        self.distance += distance

    # GERA UMA SOLUÇÃO INICIAL ALEATÓRIA
    def random_initial_solution(self):
        random.shuffle(self.clientList)
        self.initial_solution()

    # GERA UMA SOLUÇÃO INICIAL (SEM NENHUM CRITÉRIO ALÉM DA ORDEM DOS CLIENTES E DA CAPACIDADE DO VEÍCULO)

    def initial_solution(self):
        aux_clientList = self.clientList[:]
        id = 0
        while True:  # ENQUANTO EXISTIR CLIENTES NAO ADICIONADOS A MINHA ROTA
            if len(aux_clientList) == 0:
                break
            vehicle = Vehicle(id, self.capacity)
            self.vehicleList.append(vehicle)
            depot = Client(0, 0, 0)
            aux = 0
            vehicle.add_client(depot)
            while True:
                flag = vehicle.add_client(aux_clientList[-1])
                if flag == 0:
                    break
                vehicle.sum_distance_vehicle(
                    self.adjMatrix[aux][aux_clientList[-1].get_id()])
                #print(f'de {aux:^3} para {aux_clientList[-1].get_id():^3} o custo é {self.adjMatrix[aux][aux_clientList[-1].get_id()]:^9}')
                aux = aux_clientList[-1].get_id()
                aux_clientList.pop()
                if len(aux_clientList) == 0:
                    break
            id += 1
            vehicle.add_client(depot)
            vehicle.sum_distance_vehicle(self.adjMatrix[aux][0])
            self.sum_distance_instance(vehicle.get_distance())
            #print(f'distancia do veiculo: {vehicle.get_distance()}')
        #     print(f'de {aux:^3} para {0:^3} o custo é {self.adjMatrix[aux][0]:^9}')
        #     print(f'carga {vehicle.get_load()}')
        # # print(f'Total percorrido : {self.distance}')
        # print()


    # RETORNA TODOS OS CLIENTES CONTIDOS EM UMA INSTÂNCIA, COM EXCEÇÃO DO DEPÓSITO
    def get_all_clients(self):
        aux = list()
        clients = list()
        for i in self.vehicleList:
            aux.extend(i.get_route())
        for i in aux:
            if i.get_id() != 0:
                clients.append(i)
        return clients


    # SUBTRAI DA DISTANCIA TOTAL
    def decrease_distance(self, dis):
        self.distance -= dis

    # CRIA UMA ROTA TEMPORARIA 
    def create_temp_route(self, vehicle):
        vehicle.set_distance(0)
        temp_route = []
        for i in vehicle.get_route():
            temp_route.append(i)
        for i in range(len(temp_route) - 1):
            f1 = temp_route[i].get_id()
            f2 = temp_route[i + 1].get_id()
            vehicle.sum_distance_vehicle(self.adjMatrix[f1][f2]) 
        vehicle.set_route(temp_route)

    # ATUALIZA A DISTÂNCIA DA ROTA
    def update_distance(self):
        self.distance = 0
        for i in self.vehicleList:
            self.sum_distance_instance(i.get_distance())

    def remove_vehicle(self, vehicle):
        self.vehicleList.remove(vehicle)

    def add_vehicle(self, vehicle):
        self.vehicleList.append(vehicle)
