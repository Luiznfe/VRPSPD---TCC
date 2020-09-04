class Client:

    def __init__(self, id, delyvery, pick):
        self.id = id
        self.delyvery = delyvery
        self.pick = pick

    def __repr__(self):
        return str(self.id)

    def get_id(self):
        return self.id

    def get_x(self):
        return self.coorX

    def get_y(self):
        return self.coorY

    def get_delyvery(self):
        return self.delyvery

    def get_pick(self):
        return self.pick

    def set_id(self, id):
        self.id = id

    def set_x(self, x):
        self.coorX = twx

    def set_y(self, y):
        self.coorY = y

    def set_delyvery(self,delyvery):
        self.delyvery = delyvery

    def set_pick(self, pick):
        self.pick = pick

    def toString(self):
        return 'id {} delivery : {} pickup {} '.format(self.id, self.delyvery, self.pick)
