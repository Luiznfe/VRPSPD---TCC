import matplotlib.pyplot as plt

class Plot():

	def __init__(self, clients):
		self.clients = clients

	def set_clients(self, clients):
		self.clients = clients[:]

	def get_clients(self):
		return self.clients

	def plot_graph(self, clients, s):
		s.get


	
plt.plot([12.34, 22.45], [22.34, 33.56], color='green', marker='o', linestyle='dashed',linewidth=2, markersize=12)
plt.show() 
