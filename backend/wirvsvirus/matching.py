"""Model for matching of hospitals and helpers."""

from math import sqrt
from ortools.sat.python import cp_model


class MatchingModel:

    configuration: dict
    results: dict = {}

    def __init__(self, hospitals, worker):
        """Initialize matching model."""
        self.hospitals = hospitals
        self.worker = worker
        self.distances = self.calculate_distances()
        self.model = cp_model.CpModel()

    def calculate_distances(self):
        """Calculate distances betwenn worker and hospitals."""
        distances = {}
        for h in self.hospitals:
            distances[h["_id"]] = {}
            coords_h = h["location"]["coordinates"]
            for w in self.worker:
                coords_w = w["location"]["coordinates"]
                distances[h["_id"]][w["_id"]] = int(10 * sqrt((coords_h[0] - coords_w[0])**2 + (coords_h[1] - coords_w[1])**2))
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
            self.allocation[h["_id"]] = {}
            for w in self.worker:
                name = f'allocation_{h["_id"]}_{w["_id"]}'
                self.allocation[h["_id"]][w["_id"]] = self.model.NewBoolVar(name)

    def add_constraints(self):
        """Add constraints."""
        # ensure that a worker can only be allocated once to a hospital
        for w in self.worker:
            self.model.Add(sum(self.allocation[h["_id"]][w["_id"]] for h in self.hospitals) <= 1)
        # match the hospital demands based on skills
        for h in self.hospitals:
            for skill, demand in h["demand"].items():
                self.model.Add(sum(self.allocation[h["_id"]][w["_id"]] for w in self.worker if skill in w["activity_ids"]) <= demand)

    def add_objective(self):
        """Add an objective."""
        # reward each match with 100
        reward = sum(100 * self.allocation[h["_id"]][w["_id"]] for h in self.hospitals for w in self.worker)
        # penalize the sum of distances for allocated worker capacity
        distance_penalty = sum(self.distances[h["_id"]][w["_id"]] * self.allocation[h["_id"]][w["_id"]] for h in self.hospitals for w in self.worker)
        self.model.Maximize(reward - distance_penalty)

    def get_results(self):
        """Get the allocation results."""
        results = {"objective": self.solver.ObjectiveValue(),
                   "allocations": []}
        for h in self.hospitals:
            allocation = {"hospital_id": str(h["_id"]), "helper_ids": []}
            for w in self.worker:
                if self.solver.Value(self.allocation[h["_id"]][w["_id"]]) == True:
                    allocation["helper_ids"].append(str(w["_id"]))
            results["allocations"].append(allocation)
        return results
