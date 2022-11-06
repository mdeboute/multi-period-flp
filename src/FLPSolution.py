from FLPData import FLPData


class FLPSolution:
    def __init__(
        self,
        instance: FLPData,
        objective_value: int,
        x: list([list([list()])]),
        y: list([list()]),
    ):
        self.instance = instance
        self.objective_value = objective_value
        self.x = x  # x[i][j][t] = the quantity of customer j (j = 0, 1, ..., J-1) served from site i (i = 0, 1, ..., I-1) at time t (t = 0, 1, ..., T-1)
        self.y = y  # y[i][t] = 1 if site i (i = 0, 1, ..., I-1) is open at time t (t = 0, 1, ..., T-1), 0 otherwise

    def __str__(self):
        return f"FLPSolution(objective_value={self.objective_value})"

    def __repr__(self):
        return self.__str__()
