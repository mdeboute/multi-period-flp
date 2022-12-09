import mip
from FLPData import FLPData
from FLPSolution import FLPSolution


class FLPMIPModel:
    def __init__(self, instance: FLPData):
        self.instance = instance
        self.model = mip.Model(name="MPFLP", sense=mip.MINIMIZE)

        # enable to store the process log in order to get the runtime
        self.model.store_search_progress_log = True

        # Decisions variables
        # x[i][j][t] = 1 if we affect the customer j (j = 0, 1, ..., J-1) to the site i (i = 0, 1, ..., I-1) at time t (t = 0, 1, ..., T-1), 0 otherwise
        self.x = [
            [
                [
                    self.model.add_var(name=f"x_{i}_{j}_{t}", var_type=mip.BINARY)
                    for t in range(instance.T)
                ]
                for j in range(instance.J)
            ]
            for i in range(instance.I)
        ]

        # y[i][t] = 1 if we open site i (i = 0, 1, ..., I-1) at time t (t = 0, 1, ..., T-1), 0 otherwise
        self.y = [
            [
                self.model.add_var(name=f"y_{i}_{t}", var_type=mip.BINARY)
                for t in range(instance.T)
            ]
            for i in range(instance.I)
        ]

        # z[i][t] = 1 if site i (i = 0, 1, ..., I-1) is open at time t (t = 0, 1, ..., T-1), 0 otherwise
        self.z = [
            [
                self.model.add_var(name=f"z_{i}_{t}", var_type=mip.BINARY)
                for t in range(instance.T)
            ]
            for i in range(instance.I)
        ]

        # Objective function
        self.model.objective = mip.xsum(
            mip.xsum(instance.f[i][t] * self.y[i][t] for t in range(instance.T))
            for i in range(instance.I)
        ) + mip.xsum(
            mip.xsum(
                mip.xsum(
                    instance.c[i][j][t] * self.x[i][j][t] for t in range(instance.T)
                )
                for j in range(instance.J)
            )
            for i in range(instance.I)
        )

        # Constraints
        for t in range(instance.T):
            self.model += (
                mip.xsum(self.y[i][t] for i in range(instance.I)) == instance.p[t]
            )

        for i in range(instance.I):
            self.model += self.z[i][0] == self.y[i][0]
            for t in range(1, instance.T):
                self.model += self.z[i][t] == self.y[i][t] + self.z[i][t - 1]

        for t in range(instance.T):
            self.model += (
                mip.xsum(
                    mip.xsum(self.x[i][j][t] for j in range(instance.J))
                    for i in range(instance.I)
                )
                >= instance.n[t]
            )

        for j in range(instance.J):
            for t in range(1, instance.T):
                self.model += (
                    mip.xsum(self.x[i][j][t] for i in range(instance.I))
                    - mip.xsum(self.x[i][j][t - 1] for i in range(instance.I))
                    >= 0
                )

        for t in range(instance.T):
            for j in range(instance.J):
                for i in range(instance.I):
                    self.model += self.x[i][j][t] <= self.z[i][t]

        for t in range(instance.T):
            for j in range(instance.J):
                self.model += mip.xsum(self.x[i][j][t] for i in range(instance.I)) <= 1

        for i in range(instance.I):
            self.model += mip.xsum(self.y[i][t] for t in range(instance.T)) <= 1

    def _create_solution(self):
        # copy lists of variables to lists of values
        x = [
            [
                [self.x[i][j][t].x for t in range(self.instance.T)]
                for j in range(self.instance.J)
            ]
            for i in range(self.instance.I)
        ]

        y = [
            [self.y[i][t].x for t in range(self.instance.T)]
            for i in range(self.instance.I)
        ]

        z = [
            [self.z[i][t].x for t in range(self.instance.T)]
            for i in range(self.instance.I)
        ]

        return x, y, z

    def solve(
        self,
        solver_name: str = "GRB",
        verbose: bool = True,
        time_limit: int = 600,
        max_gap: float = 0.0001,
        nb_threads: int = -1,
    ) -> FLPSolution:
        self.model.solver_name = solver_name
        self.model.verbose = int(verbose)
        self.model.max_seconds = time_limit
        self.model.max_mip_gap = max_gap
        self.model.threads = nb_threads
        # Solve model
        _status = self.model.optimize()

        # Create solution
        _x, _y, _z = self._create_solution()
        _runtime = self.model.search_progress_log.log[-1][0]

        # Get solution
        if _status == mip.OptimizationStatus.OPTIMAL:
            print(
                f"Optimal Result: runtime={_runtime:.2f}sec; objective={int(self.model.objective_value)}"
            )
            return FLPSolution(
                self.instance, int(self.model.objective_value), _x, _y, _z
            )
        elif _status == mip.OptimizationStatus.FEASIBLE:
            print(
                f"Result: runtime={_runtime:.2f}sec; objective={int(self.model.objective_value)}"
            )
            return FLPSolution(
                self.instance, int(self.model.objective_value), _x, _y, _z
            )
        else:
            print("No solution found!")

    def __str__(self):
        return f"FLPMIPModel(instance={self.instance})"

    def __repr__(self):
        return self.__str__()
