POTENTIAL_RANGE = 110000 # Resting potential: -70 mV Membrane potential range: +40 mV to -70 mV --- Difference: 110 mV = 110000 microVolt --- https://en.wikipedia.org/wiki/Membrane_potential
ACTION_POTENTIAL = 15000 # Resting potential: -70 mV Action potential: -55 mV --- Difference: 15mV = 15000 microVolt --- https://faculty.washington.edu/chudler/ap.html

# https://en.wikipedia.org/wiki/Neuron
# https://en.wikipedia.org/wiki/Dendritic_spine

class Neuron():

	total_neurons = 0

	def __init__(self, dendritic_spine_count=0, axon_terminal_count=0):
		self.dendritic_spine_count = dendritic_spine_count
		self.dendritic_spines = []
		self.axon_terminal_count = axon_terminal_count
		self.axon_terminals = []

		Neuron.total_neurons += 1

		for i in xrange(dendritic_spine_count):
			self.dendritic_spines.append(DendriticSpine())
		for i in xrange(axon_terminal_count):
			self.axon_terminals.append(AxonTerminal())

		print self.axon_terminals
		print self.dendritic_spines

class DendriticSpine():

	def __init__(self, axon_terminal=None, excitement=0):
		if isinstance(axon_terminal, DendriticSpine):
			self.axon_terminal = None
		else:
			self.axon_terminal = axon_terminal
		self.excitement = excitement

class AxonTerminal():

	def __init__(self, dendritic_spine=None, excitement=0):
		if isinstance(dendritic_spine, AxonTerminal):
			self.dendritic_spine = None
		else:
			self.dendritic_spine = dendritic_spine
		self.excitement = excitement
