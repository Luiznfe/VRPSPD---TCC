from instance import Instance
class Population:

    def __init__(self):
        self.instances = list()

    def set_instances(self, instances):
        self.instances = instances[:]

    def get_instances(self):
        return self.instances[:]

    def generate_population(self, n, path):
        for i in range(n):
            instance = Instance()
            instance.set_instance(path)
            instance.random_initial_solution()
            self.instances.append(instance)
