from FLPData import FLPData
from FLPSolution import FLPSolution
import time


class FLPHeuristic:
    def __init__(self, instance: FLPData):
        self.instance = instance

    def _solve_open_sites(self):
        # this method solves the open sites problem for each period
        # we want to open p_t sites by minimizing their opening cost
        # we use the greedy algorithm to solve this problem

        # create the list of sites to open at each period
        open_sites = [
            [0 for _ in range(self.instance.T)] for _ in range(self.instance.I)
        ]

        unopened_sites = [i for i in range(self.instance.I)]

        # for each period
        for t in range(self.instance.T):
            # create a list of tuples (site, opening cost) and sort it by opening cost
            sites = [(i, self.instance.f[i][t]) for i in unopened_sites]
            sites.sort(key=lambda x: x[1])

            # open the first p_t sites but only if they are not already open
            for i in range(self.instance.p[t]):
                for t_ in range(t, self.instance.T):
                    open_sites[sites[i][0]][t_] = 1
                # delete the site from the list
                unopened_sites.remove(sites[i][0])

        return open_sites

    def _get_assignement_cost(self, open_sites):
        # create a list of size J X T to store the assignment cost
        assignment_cost = [
            [0 for _ in range(self.instance.T)] for _ in range(self.instance.J)
        ]

        # assignment_cost[j][t] = sum of the minimum assignment cost of the sites that are open at period t' for t' = t to T
        for j in range(self.instance.J):
            for t in range(self.instance.T):
                assignment_cost[j][t] = sum(
                    min(
                        self.instance.c[i][j][t_]
                        for i in range(self.instance.I)
                        if open_sites[i][t_] == 1
                    )
                    for t_ in range(t, self.instance.T)
                )

        return assignment_cost

    def _solve_assignement(self, assignement_cost):
        # create a list of size J X T to store the assignment
        assignments = [
            [0 for _ in range(self.instance.T)] for _ in range(self.instance.J)
        ]

        # for each period
        for t in range(self.instance.T):
            # create a list of tuples (customer, assignment cost) and sort it by assignment cost
            customers = [(j, assignement_cost[j][t]) for j in range(self.instance.J)]
            customers.sort(key=lambda x: x[1])

            # assign the first n_t customers if they are not already assigned
            # customers are assigned at most once
            for j in range(self.instance.n[t]):
                if assignments[customers[j][0]][t] == 0:
                    assignments[customers[j][0]][t] = 1

        return assignments

    def _get_objective_value(self, open_sites, assignments, assignment_cost):
        # compute the objective value
        objective_value = 0

        # opening cost (we only count this cost once per sites opened)
        for i in range(self.instance.I):
            for t in range(self.instance.T):
                if open_sites[i][t] == 1:
                    objective_value += self.instance.f[i][t]
                    break

        # assignment cost
        for j in range(self.instance.J):
            for t in range(self.instance.T):
                objective_value += assignment_cost[j][t] * assignments[j][t]

        return objective_value

    def _create_solution(self, open_sites, assignments):
        # x[i][j][t] = 1 if we affect the customer j (j = 0, 1, ..., J-1) to the site i (i = 0, 1, ..., I-1) at time t (t = 0, 1, ..., T-1), 0 otherwise
        x = [
            [[0 for _ in range(self.instance.T)] for _ in range(self.instance.J)]
            for _ in range(self.instance.I)
        ]

        for t in range(self.instance.T):
            for j in range(self.instance.J):
                if assignments[j][t] == 1:
                    for nt in range(t, self.instance.T):
                        least_cost_site = -1
                        least_cost = 0
                        for i in range(self.instance.I):
                            if open_sites[i][nt] == 1 and (
                                self.instance.c[i][j][nt] < least_cost
                                or least_cost_site == -1
                            ):
                                least_cost = self.instance.c[i][j][nt]
                                least_cost_site = i
                        if least_cost_site != -1:
                            x[least_cost_site][j][nt] = 1
                        else:
                            print("Failed to assign customer", j, "at period", nt)

        # z[i][t] = 1 if site i (i = 0, 1, ..., I-1) is open at time t (t = 0, 1, ..., T-1), 0 otherwise
        z = open_sites

        # y[i][t] = 1 if we open site i (i = 0, 1, ..., I-1) at time t (t = 0, 1, ..., T-1), 0 otherwise
        y = [[0 for _ in range(self.instance.T)] for _ in range(self.instance.I)]

        for i in range(self.instance.I):
            for t in range(self.instance.T):
                if z[i][t] == 1:
                    y[i][t] = 1
                    break

        return x, y, z

    def solve(self, time_limit: int = 600):
        # start the timer
        _start_time = time.time()

        while time.time() - _start_time < time_limit:
            # solve the open sites problem
            open_sites = self._solve_open_sites()

            # compute the assignment cost
            assignment_cost = self._get_assignement_cost(open_sites)

            # solve the assignment problem
            assignments = self._solve_assignement(assignment_cost)

            # compute the objective value
            objective_value = self._get_objective_value(
                open_sites,
                assignments,
                assignment_cost,
            )

            print("Solution found in {0:.2f} seconds".format(time.time() - _start_time))

            # create the solution
            x, y, z = self._create_solution(open_sites, assignments)

            return FLPSolution(self.instance, objective_value, x, y, z)

        print("No solution found in {0:.2f} seconds".format(time.time() - _start_time))
        exit(1)
