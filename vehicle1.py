from random import randint
class Vehicle:

    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.route = list()
        self.distance = 0
        self.load = 0

    def __repr__(self):
        return str(self.id)

    def get_id(self):
        return self.id

    def get_load(self):
        return self.load

    def get_capacity(self):
        return self.capacity

    def get_route(self):
        return self.route[:]

    def get_distance(self):
        return self.distance

    def set_id(self, id):
        self.id = id

    def set_capacity(self, capacity):
        self.capacity = capacity

    def set_route(self, route):
        self.route.clear()
        self.route = route[:]

    def set_distance(self, distance):
        self.distance = distance

    def toString(self):
        return 'id : {} distance : {} capacity : {} '.format(self.id, self.distance, self.capacity)

    # ADICIONA UM ELEMENTO A LISTA

    def add_client(self, client):
        temp = self.load
        temp += client.get_delyvery()
        if temp > self.capacity:
            return 0
        temp -= client.get_delyvery()
        temp += client.get_pick()
        if temp > self.capacity:
            return 0
        self.load = temp
        self.route.append(client)

    # REMOVE CLIENTES DA ROTA

    def remove_client(self, x):
        self.route.remove(x)

    # SOMA A NOVA DISTANCIA AO TOTAL

    def sum_distance_vehicle(self, x):
        self.distance += x

    # VERIFICA SE UMA ROTA É VÁLIDA
    def is_feasible(self):
        load = 0
        for i in self.route:
            load += i.get_delyvery()
        for i in self.route:
            load -= i.get_delyvery()
            load += i.get_pick()
            if load > self.capacity:
                return 0
        return 1

    # ADICIONA UM CLINTE SEM CONFERIR SE É POSSÍVEL
    def add(self, client):
        self.route.insert(randint(1, len(self.route) - 2), client)

    def get_index(self, x):
        for i in range(len(self.route)):
            if self.route[i].get_id() == x.get_id():
                return i