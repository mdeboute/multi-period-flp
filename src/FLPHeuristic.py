from FLPData import FLPData


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

        # for each period
        for t in range(self.instance.T):
            # create a list of tuples (site, opening cost) and sort it by opening cost
            sites = [(i, self.instance.f[i][t]) for i in range(self.instance.I)]
            sites.sort(key=lambda x: x[1])

            # open the first p_t sites but only if they are not already open
            for i in range(self.instance.p[t]):
                open_sites[sites[i][0]][t] = 1
                # delete the site from the list
                del sites[i]

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
                        self.instance.c[i][j][_t]
                        for i in range(self.instance.I)
                        if open_sites[i][_t] == 1
                    )
                    for _t in range(t, self.instance.T)
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
            for j in range(self.instance.n[t]):
                if assignments[customers[j][0]][t] == 0:
                    assignments[customers[j][0]][t] = 1

        return assignments

    def _get_objective_value(self, open_sites, assignments):
        # compute the objective value
        objective_value = 0

        # opening cost
        for i in range(self.instance.I):
            for t in range(self.instance.T):
                objective_value += self.instance.f[i][t] * open_sites[i][t]

        # assignment cost
        for j in range(self.instance.J):
            for t in range(self.instance.T):
                objective_value += self.instance.c[i][j][t] * assignments[j][t]

        return objective_value

    def solve(self):
        # solve the open sites problem
        open_sites = self._solve_open_sites()

        # compute the assignment cost
        assignment_cost = self._get_assignement_cost(open_sites)

        # solve the assignment problem
        assignments = self._solve_assignement(assignment_cost)

        # compute the objective value
        objective_value = self._get_objective_value(open_sites, assignments)

        return objective_value
