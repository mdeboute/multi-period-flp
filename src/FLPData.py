class FLPData:
    def __init__(
        self,
        I: int,
        J: int,
        T: int,
        n: list(),
        p: list(),
        f: list([list()]),
        c: list([list([list()])]),
    ):
        self.I = I  # number of sites (i = 0, 1, ..., I-1)
        self.J = J  # number of customers (j = 0, 1, ..., J-1)
        self.T = T  # number of time (t = 0, 1, ..., T-1)
        self.n = n  # number of customers to be served at time t (t = 0, 1, ..., T-1)
        self.p = p  # number of sites to be opened at time t (t = 0, 1, ..., T-1)
        self.f = f  # fixed cost of opening a site i (i = 0, 1, ..., I-1) at time t (t = 0, 1, ..., T-1)
        self.c = c  # cost of serving a customer j (j = 0, 1, ..., J-1) from site i (i = 0, 1, ..., I-1) at time t (t = 0, 1, ..., T-1)

    def __str__(self):
        return f"FLPData(I={self.I}, J={self.J}, T={self.T}, n={self.n}, p={self.p}, f={self.f}, c={self.c})"

    def __repr__(self):
        return self.__str__()
