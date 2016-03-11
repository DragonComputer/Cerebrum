 

from cerebrum.neuralnet.utilities import abstractMethod
from cerebrum.neuralnet.optimization.optimizer import BlackBoxOptimizer


class Evolution(BlackBoxOptimizer):
    """ Base class for evolutionary algorithms, seen as function optimizers. """

    populationSize = 10

    storeAllPopulations = False

    mustMaximize = True

    def _additionalInit(self):
        self.currentpop = []
        self.fitnesses = []
        self._allGenerations = []
        self.initPopulation()

    def _learnStep(self):
        """ do one generation step """
        self.fitnesses = [self._oneEvaluation(indiv) for indiv in self.currentpop]
        if self.storeAllPopulations:
            self._allGenerations.append((self.currentpop, self.fitnesses))
        self.produceOffspring()

    def initPopulation(self):
        """ initialize the population """
        abstractMethod()

    def produceOffspring(self):
        """ generate the new generation of offspring, given the current population, and their fitnesses """
        abstractMethod()

    @property
    def batchSize(self):
        return self.populationSize