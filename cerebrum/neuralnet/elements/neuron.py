import random
import itertools
import time
from threading import Thread

POTENTIAL_RANGE = 110000 # Resting potential: -70 mV Membrane potential range: +40 mV to -70 mV --- Difference: 110 mV = 110000 microVolt --- https://en.wikipedia.org/wiki/Membrane_potential
ACTION_POTENTIAL = 15000 # Resting potential: -70 mV Action potential: -55 mV --- Difference: 15mV = 15000 microVolt --- https://faculty.washington.edu/chudler/ap.html
AVERAGE_SYNAPSES_PER_NEURON = 8200 # The average number of synapses per neuron: 8,200 --- http://www.ncbi.nlm.nih.gov/pubmed/2778101

# https://en.wikipedia.org/wiki/Neuron

class Neuron():

	neurons = []

	def __init__(self):
		self.dendritic_spines = {}
		self.axon_terminals = {}
		self.potential = 0
		#self.create_dendritic_spines()
		#self.create_axon_terminals()
		Neuron.neurons.append(self)
		self.thread = Thread(target = self.activate)
		self.thread.start()

	def create_dendritic_spines(self):
		for neuron in Neuron.neurons[len(self.dendritic_spines):]:
			if id(neuron) != id(self):
				self.dendritic_spines[id(neuron)] = random.uniform(0.0, 1.0)

	def create_axon_terminals(self):
		for neuron in Neuron.neurons[len(self.axon_terminals):]:
			if id(neuron) != id(self):
				self.axon_terminals[id(neuron)] = random.uniform(0.0, 1.0)

	def activate(self):
		while True:
			'''
			for dendritic_spine in self.dendritic_spines:
				if dendritic_spine.axon_terminal is not None:
					dendritic_spine.potential = dendritic_spine.axon_terminal.potential
					print dendritic_spine.potential
				self.neuron_potential += dendritic_spine.potential * dendritic_spine.excitement
			terminal_potential = self.neuron_potential / len(self.axon_terminals)
			for axon_terminal in self.axon_terminals:
				axon_terminal.potential = terminal_potential
			'''
			time.sleep(2)
			pass

			'''
			if abs(len(Neuron.neurons) - len(self.dendritic_spines) + 1) > 0:
				self.create_dendritic_spines()

			if abs(len(Neuron.neurons) - len(self.axon_terminals) + 1) > 0:
				self.create_axon_terminals()
			'''

class Build():

	def __init__(self):
		for i in range(1000):
			Neuron()
		map(lambda x: x.create_dendritic_spines(),Neuron.neurons)
		map(lambda x: x.create_axon_terminals(),Neuron.neurons)
