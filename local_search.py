import copy
from vehicle import Vehicle
from random import randint, sample
from two_opt import TwoOpt
class LS:


    def local_search(self, s, maxIter):
        f = iter = 0
        print(s.get_distance())
        self.swap_01(s)
       
        self.shift_02(s)
        while True:
            f = self.swap_01(s)
            iter += 1
            if f == 1 or iter == maxIter:
                break
        iter = 0
        while True:
            f = self.swap_02(s)
            iter += 1
            if f == 1 or iter == maxIter:
                break
        iter = 0
        while True:
            f = self.swap_03(s)
            iter += 1
            if f == 1 or iter == maxIter:
                break
        opt = TwoOpt()
        for i in s.get_vehicleList():
            opt.run_two_opt(i, s)
            
        print(s.get_distance())
        return s

    # INSERE UM CLIENTE DE R1 EM R2
    # # PEGA UM CLIENTE DA ROTA R1 E INSERE NA PRIMEIRA MELHOR POSIÇÃO NA ROTA R2
    def shift_01(self, s):
        # s1 = copy.deepcopy(s)
        f = 0
        vehicle_1, vehicle_2 = sample(s.get_vehicleList(), 2)
        for i in range(1, len(vehicle_1.get_route()) - 1):
            client = vehicle_1.get_route()[i]
            for j in range(1, len(vehicle_2.get_route())):
                f = self.insert_shift_01(client, i, j, vehicle_1, vehicle_2, s)
                if f == 1:
                    s.update_distance()
                    return 1
    # INSERE O CLIENTE C EM R2, APAGA C DE R1 E VERIFICA SE EXISTIU MELHORA
    # COMPARA AS DISTANCIAS ANTES DE ANTES E DEPOIS DA TROCA
    def insert_shift_01(self, client, i, j, vehicle_1, vehicle_2, s1):
        previous_distance = vehicle_1.get_distance() + vehicle_2.get_distance()
        vehicle_2.insert_client(j, client)
        vehicle_1.remove_client(client)
        if vehicle_1.is_feasible() * vehicle_2.is_feasible() == 1:
            s1.create_temp_route(vehicle_1)
            s1.create_temp_route(vehicle_2)
            new_distance = vehicle_1.get_distance() + vehicle_2.get_distance()
            if new_distance < previous_distance:
                return 1

        vehicle_2.remove_client(client)
        vehicle_1.insert_client(i, client)
        s1.create_temp_route(vehicle_1)
        s1.create_temp_route(vehicle_2)
        return 0
        
    # # DOIS CLIENTES CONSECUTIVOS i E j SÃO TRANSFERIDOS DE UMA ROTA R1 PARA R2
    def shift_02(self, s):
        r1, r2 = sample(s.get_vehicleList(), 2)
        f = 0
        if len(r1.get_route()) <= 3:
            return 0
        for i in range(1, len(r1.get_route()) - 2):
            client_1 = r1.get_route()[i]
            client_2 = r1.get_route()[i + 1]
            for j in range(1, len(r2.get_route())):
                f = self.insert_shift_02(client_1, client_2, i, j, r1, r2, s)
                if f == 1:
                    s.update_distance()
                    return 1
    # FAZ A TROCA E VERIFICA SE EXISTIU MELHORA
    def insert_shift_02(self, c1, c2, i, j, v1, v2, s1):
        previous_distance = v1.get_distance() + v2.get_distance()
        v2.add_consecutive(c1, c2, j)
        v1.remove_client(c1)
        v1.remove_client(c2)
        if v1.is_feasible() * v2.is_feasible() == 1:
            s1.create_temp_route(v1)
            s1.create_temp_route(v2)
            new_distance = v1.get_distance() + v2.get_distance()
            if new_distance < previous_distance:
                return 1
        v1.add_consecutive(c1, c2, i)
        v2.remove_client(c1)
        v2.remove_client(c2)
        s1.create_temp_route(v1)
        s1.create_temp_route(v2)
        return 0


    # # UM CLIENTE i DA ROTA R1 É PERMUTADO COM O CLINTE j DA ROTA R2
    def swap_01(self, s):
        s1 = copy.deepcopy(s)
        r1, r2 = sample(s1.get_vehicleList(), 2)

        previous_distance = r1.get_distance() + r2.get_distance()

        client_1 = r1.get_route()[randint(1, len(r1.get_route()) - 2)]
        c1_index = r1.get_route().index(client_1)
        client_2 = r2.get_route()[randint(1, len(r2.get_route()) - 2)]
        c2_index = r2.get_route().index(client_2)

        r1.remove_client(client_1)
        r2.remove_client(client_2)
        r1.insert_client(c1_index, client_2)
        r2.insert_client(c2_index, client_1)
        flag = self.verify_new_route_swap(r1, r2, s1, s, previous_distance)
        return flag 

    # VERIFICA SE A NOVA ROTA É MENOR E FAZ A TROCA CASO SEJA
    def verify_new_route_swap(self, r1, r2, s1, s, previous_distance):
        a = r1.is_feasible()
        b = r2.is_feasible()
        if a == 1 and b == 1:
            s1.create_temp_route(r1)
            s1.create_temp_route(r2)
            new_distance = r1.get_distance() + r2.get_distance()
            if new_distance < previous_distance:
                s1.update_distance()
                s.set_vehicleList(s1.get_vehicleList())
                s.set_distance(s1.get_distance())
                return 1
            else:
                return 0
        else:
            return 0


    # DOIS CLIENTES CONSECUTIVOS I E J DA ROTA 1 SÃO PERMUTADOS COM UM CIENTE K DE R2
    def swap_02(self, s):
        s1 = copy.deepcopy(s)
        r1, r2 = sample(s1.get_vehicleList(), 2)
        if len(r1.get_route()) <= 3:
            return 0

        previous_distance = r1.get_distance() + r2.get_distance()

        index_1 = randint(1, len(r1.get_route()) - 3)
        client_1 = r1.get_route()[index_1]
        client_2 = r1.get_route()[index_1 + 1]

        index_2 = randint(1, len(r2.get_route()) - 2)
        client_3 = r2.get_route()[index_2]

        r1.remove_client(client_1)
        r1.remove_client(client_2)
        r2.remove_client(client_3)

        r1.insert_client(index_1, client_3)
        r2.insert_client(index_2, client_1)
        r2.insert_client(index_2 + 1, client_2)

        flag = self.verify_new_route_swap(r1, r2, s1, s, previous_distance)
        return flag 

    # DOIS CLIENTES CONSECUTIVOS DE R1 SÃO PERMUTADOS COM OUTROS DOIS CLIENTES
    # CONSECUTIVOS DE R2
    def swap_03(self, s):
        s1 = copy.deepcopy(s)
        r1, r2 = sample(s1.get_vehicleList(), 2)

        if len(r1.get_route()) <= 3 or len(r2.get_route()) <= 3:
            return 0

        previous_distance = r1.get_distance() + r2.get_distance()

        index_1 = randint(1, len(r1.get_route()) - 3)
        client_1 = r1.get_route()[index_1]
        client_2 = r1.get_route()[index_1 + 1]

        index_2 = randint(1, len(r2.get_route()) - 3)
        client_3 = r2.get_route()[index_2]
        client_4 = r2.get_route()[index_2 + 1]

        r1.remove_client(client_1)
        r1.remove_client(client_2)

        r1.insert_client(index_1, client_3)
        r1.insert_client(index_1 + 1, client_4)

        r2.insert_client(index_2, client_1)
        r2.insert_client(index_2 + 1, client_2)

        flag = self.verify_new_route_swap(r1, r2, s1, s, previous_distance)
        return flag
