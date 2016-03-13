POTENTIAL_RANGE = 110000 # Resting potential: -70 mV Membrane potential range: +40 mV to -70 mV --- Difference: 110 mV = 110000 microVolt --- https://en.wikipedia.org/wiki/Membrane_potential
ACTION_POTENTIAL = 15000 # Resting potential: -70 mV Action potential: -55 mV --- Difference: 15mV = 15000 microVolt --- https://faculty.washington.edu/chudler/ap.html
AVERAGE_SYNAPSES_PER_NEURON = 8200 # The average number of synapses per neuron: 8,200 --- http://www.ncbi.nlm.nih.gov/pubmed/2778101

# https://en.wikipedia.org/wiki/Neuron

class Neuron():

	total_neurons = 0

	def __init__(self, dendritic_spine_count=AVERAGE_SYNAPSES_PER_NEURON/2, axon_terminal_count=AVERAGE_SYNAPSES_PER_NEURON/2):
		self.dendritic_spine_count = dendritic_spine_count
		self.axon_terminal_count = axon_terminal_count
		self.neuron_potential = 0
		self.dendrit_constructor(self.dendritic_spine_count)
		self.axon_constructor(self.axon_terminal_count)

		Neuron.total_neurons += 1


	def dendrit_constructor(self, dendritic_spine_count):
		self.dendritic_spines = []
		for i in xrange(dendritic_spine_count):
			self.dendritic_spines.append(DendriticSpine())
		print len(self.dendritic_spines)

	def axon_constructor(self, axon_terminal_count):
		self.axon_terminals = []
		for i in xrange(axon_terminal_count):
			self.axon_terminals.append(AxonTerminal())
		print len(self.axon_terminals)

	def activate(self):
		while True:
			for dendritic_spine in self.dendritic_spines:
				dendritic_spine.potential = dendritic_spine.axon_terminal.potential
				print dendritic_spine.potential
				self.neuron_potential += dendritic_spine.potential
			terminal_potential = self.neuron_potential / len(axon_terminals)
			for axon_terminal in self.axon_terminals:
				axon_terminal.potential = terminal_potential

# https://en.wikipedia.org/wiki/Dendritic_spine

class DendriticSpine():

	def __init__(self, axon_terminal=None, excitement=0, potential=0):
		if isinstance(axon_terminal, DendriticSpine):
			self.axon_terminal = None
		else:
			self.axon_terminal = axon_terminal
		self.potential = potential
		self.excitement = excitement

# https://en.wikipedia.org/wiki/Dendritic_spine

class AxonTerminal():

	def __init__(self, dendritic_spine=None, excitement=0, potential=0):
		if isinstance(dendritic_spine, AxonTerminal):
			self.dendritic_spine = None
		else:
			self.dendritic_spine = dendritic_spine
		self.potential = potential
		self.excitement = excitement

# https://faculty.washington.edu/chudler/cells.html

class SensoryNeuron(Neuron):

	def dendrit_constructor(self, dendritic_spine_count):
		self.dendritic_spines = []
		for i in xrange(dendritic_spine_count):
			self.dendritic_spines.append(DendriticSpine())
		self.dendritic_spines = tuple(self.dendritic_spines)
		print len(self.dendritic_spines)
