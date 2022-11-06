import mip
from FLPData import FLPData
from FLPSolution import FLPSolution


class FLPMIPModel:
    def __init__(self, instance: FLPData):
        self.instance = instance
        self.model = mip.Model(name="MPFLP", sense=mip.MINIMIZE)

        # Decisions variables
        self.x = [
            [
                [
                    self.model.add_var(name=f"x_{i}_{j}_{t}", var_type=mip.INTEGER)
                    for t in range(instance.T)
                ]
                for j in range(instance.J)
            ]
            for i in range(instance.I)
        ]

        self.y = [
            [
                self.model.add_var(name=f"y_{i}_{t}", var_type=mip.BINARY)
                for t in range(instance.T)
            ]
            for i in range(instance.I)
        ]

        # Objective function
        self.model.objective = mip.xsum(
            mip.xsum(self.instance.f[i][t] * self.y[i][t] for t in range(instance.T))
            for i in range(instance.I)
        ) + mip.xsum(
            mip.xsum(
                mip.xsum(
                    self.instance.c[i][j][t] * self.x[i][j][t]
                    for t in range(instance.T)
                )
                for j in range(instance.J)
            )
            for i in range(instance.I)
        )

        # Constraints
        for t in range(instance.T):
            for j in range(instance.J):
                self.model += mip.xsum(self.x[i][j][t] for i in range(instance.I)) == 1

        for t in range(instance.T):
            for i in range(instance.I):
                self.model += mip.xsum(self.x[i][j][t] for j in range(instance.J)) <= (
                    self.instance.n[t] * self.y[i][t]
                )

        for t in range(instance.T):
            self.model += (
                mip.xsum(self.y[i][t] for i in range(instance.I)) == self.instance.p[t]
            )

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
        status = self.model.optimize()

        # Get solution
        if status == mip.OptimizationStatus.OPTIMAL:
            return FLPSolution(
                self.instance, self.model.objective_value, self.x, self.y
            )
        else:
            return FLPSolution(self.instance, float("inf"), self.x, self.y)
