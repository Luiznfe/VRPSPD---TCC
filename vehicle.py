from random import randint
class Vehicle:

    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.route = list()
        self.distance = 0

    def __repr__(self):
        return str(self.id)

    def get_id(self):
        return self.id

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

    def add_client(self, x):
        load = 0
        self.route.append(x)
        for i in self.route:
            load += i.get_delyvery()
        if load > self.capacity:
            self.route.pop()
            return 0
        for i in self.route:
            load -= i.get_delyvery()
            load += i.get_pick()
            if load > self.capacity:
                self.route.pop()
                return 0
        return 1

    # REMOVE CLIENTES DA ROTA

    def remove_client(self, c):
        for i in self.route:
            if i.get_id() == c.get_id():
                self.route.remove(i) 
                return 1
        return 0    

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

    # ADICIONA UM CLINTE ALEATORIAMENTE SEM CONFERIR SE É POSSÍVEL
    def insert_client(self, index, client):
        self.route.insert(index, client)


    # ADICIONA 2 CLIENTES CONSECUTIVAMENTES EM UMA LISTA
    def add_consecutive(self, client1, client2, index):
        self.route.insert(index, client1)
        self.route.insert(index + 1, client2)

    def get_index(self, x):
        for i in range(len(self.route)):
            if self.route[i].get_id() == x.get_id():
                return i
