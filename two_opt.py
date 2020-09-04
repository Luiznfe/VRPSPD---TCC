from threading import Thread
import copy

class TwoOpt(Thread):

    def run_two_opt(self, vehicle, s):
        # for j in vehicle.get_route():
        #     print(j, end=" ")
        # print()
        vehicle_test = copy.deepcopy(s.get_vehicleList()[0])
        new_route = self.two_opt(vehicle.get_route(), s, vehicle_test)
        vehicle.set_route(new_route)
        # for i in vehicle.get_route():
        # 	print(i, end=" ")

    def cost(self, new_route, s, vehicle):
        vehicle.set_route(new_route)
        a = vehicle.is_feasible()
        if a == 0:
            return vehicle.get_distance() * 1000
        s.create_temp_route(vehicle)
        return vehicle.get_distance()

    def two_opt(self, route, s, vehicle_test):
        best = route
        improved = True
        while improved:
            improved = False
            for i in range(1, len(route) - 2):
                for j in range(i + 1, len(route)):
                    if j - i == 1:
                        continue
                    new_route = route[:]
                    new_route[i:j] = route[j - 1:i - 1:-1]
                    if self.cost(new_route, s, vehicle_test) < self.cost(best, s, vehicle_test):
                        # print()
                        # for k in new_route:
                        #     print(k, end=" ")
                        # print()
                        best = new_route
                        improved = True
            route = best
        return best
