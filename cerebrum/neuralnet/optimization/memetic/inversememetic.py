 

from .memetic import MemeticSearch


class InverseMemeticSearch(MemeticSearch):
    """ Interleaving local search with topology search (inverse of memetic search) """

    def _learnStep(self):
        self.switchMutations()
        MemeticSearch._learnStep(self)
        self.switchMutations()
