"""Model for matching of hospitals and helpers."""

from math import sqrt
from ortools.sat.python import cp_model


class MatchingModel:

    configuration: dict
    results: dict = {}

    def __init__(self, configuration):
        """Initialize matching model."""
        self.configuration = configuration
        self.hospitals = configuration["hospitals"]
        self.worker = configuration["worker"]
        self.distances = self.calculate_distances()
        self.model = cp_model.CpModel()

    def calculate_distances(self):
        """Calculate distances betwenn worker and hospitals."""
        distances = {}
        for h in self.hospitals:
            distances[h["name"]] = {}
            for w in self.worker:
                distances[h["name"]][w["name"]] = int(10 * sqrt((h["latitude"] - w["latitude"])**2 + (h["longitude"] - w["longitude"])**2))
        return distances

    def solve(self):
        """Solve matching model."""
        self.create_variables()
        self.add_constraints()
        self.add_objective()
        self.solver = cp_model.CpSolver()
        status = self.solver.Solve(self.model)
        self.results = self.get_results()

    def create_variables(self):
        """Create allocation variables."""
        self.allocation = {}
        for h in self.hospitals:
            self.allocation[h["name"]] = {}
            for w in self.worker:
                name = f'allocation_{h["name"]}_{w["name"]}'
                self.allocation[h["name"]][w["name"]] = self.model.NewBoolVar(name)

    def add_constraints(self):
        """Add constraints."""
        # ensure that a worker can only be allocated once to a hospital
        for w in self.worker:
            self.model.Add(sum(self.allocation[h["name"]][w["name"]] for h in self.hospitals) <= 1)
        # match the hospital demands based on skills
        for h in self.hospitals:
            for skill, demand in h["demand"].items():
                self.model.Add(sum(self.allocation[h["name"]][w["name"]] for w in self.worker if w["skill"] == skill) <= demand)

    def add_objective(self):
        """Add an objective."""
        # reward each match with 100
        reward = sum(100 * self.allocation[h["name"]][w["name"]] for h in self.hospitals for w in self.worker)
        # penalize the sum of distances for allocated worker capacity
        distance_penalty = sum(self.distances[h["name"]][w["name"]] * self.allocation[h["name"]][w["name"]] for h in self.hospitals for w in self.worker)
        self.model.Maximize(reward - distance_penalty)

    def get_results(self):
        """Get the allocation results."""
        results = {"objective": self.solver.ObjectiveValue(),
                   "allocation": {}}
        for h in self.hospitals:
            results["allocation"][h["name"]] = []
            for w in self.worker:
                if self.solver.Value(self.allocation[h["name"]][w["name"]]) == True:
                    results["allocation"][h["name"]].append(w["name"])
        return results
