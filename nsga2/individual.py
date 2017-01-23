"""Module with main parts of NSGA-II algorithm.
It contains individual definition"""

class Individual(object):
    """Represents one individual"""
    
    def __init__(self):
        self.rank = None
        self.crowding_distance = 0
        self.dominated_solutions = set()
        self.features = None
        self.normalized_objectives = None
        self.objectives = None
        self.dominates = None

    def set_objectives(self, objectives):
        self.objectives = objectives
