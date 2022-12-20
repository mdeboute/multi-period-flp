from FLPData import FLPData
from pathlib import Path


class FLPSolution:
    __BASE_DIR = Path(__file__).resolve().parent.parent

    def __init__(
        self,
        instance: FLPData,
        algorithm: str,
        objective_value: int,
        x: list([list([list()])]),
        y: list([list()]),
        z: list([list()]),
    ):
        self.instance = instance
        self.algorithm = algorithm
        self.objective_value = objective_value
        self.x = x  # x[i][j][t] = 1 if we affect the customer j (j = 0, 1, ..., J-1) to the site i (i = 0, 1, ..., I-1) at time t (t = 0, 1, ..., T-1), 0 otherwise
        self.y = y  # y[i][t] = 1 if we open site i (i = 0, 1, ..., I-1) at time t (t = 0, 1, ..., T-1), 0 otherwise
        self.z = z  # z[i][t] = 1 if site i (i = 0, 1, ..., I-1) is open at time t (t = 0, 1, ..., T-1), 0 otherwise
        self.__SOLUTION_DIR = str(self.__BASE_DIR) + "/solution/" + self.algorithm

    def __str__(self):
        return f"FLPSolution(objective_value={self.objective_value})"

    def __repr__(self):
        return self.__str__()

    def _get_sites_period(self):
        # we want to know from which period each site is open
        # example: [2, 1, 1, 2] means that site 0 is open from period 2, site 1 from period 1, site 2 from period 1 and site 3 from period 2
        sites_period = [0 for _ in range(self.instance.I)]
        for i in range(self.instance.I):
            for t in range(self.instance.T):
                if self.z[i][t] == 1 and sites_period[i] == 0:
                    sites_period[i] = t + 1
                    break
        return sites_period

    def _get_customers_period(self):
        # we want to know from which period each customer is covered
        # example: [2, 1, 1, 2] means that customer 0 is covered from period 2, customer 1 from period 1, customer 2 from period 1 and customer 3 from period 2
        customers_period = [0 for _ in range(self.instance.J)]
        for j in range(self.instance.J):
            for t in range(self.instance.T):
                for i in range(self.instance.I):
                    if self.x[i][j][t] == 1 and customers_period[j] == 0:
                        customers_period[j] = t + 1
                        break
        return customers_period

    def check_feasibility(self):
        # check that the solution is feasible
        # 1. check that for each customer, for each period, the sum of x[i][j][t] <= 1 for i = 0, 1, ..., I-1
        for j in range(self.instance.J):
            for t in range(self.instance.T):
                sum_x = 0
                for i in range(self.instance.I):
                    sum_x += self.x[i][j][t]
                if sum_x > 1:
                    print(
                        f"ERROR: for customer {j} at period {t}, the sum of x[i][j][t] on i is {sum_x} > 1"
                    )
                    return False

        # 2. check that for each site, for each customer, for each period, x[i][j][t] <= z[i][t]
        for i in range(self.instance.I):
            for j in range(self.instance.J):
                for t in range(self.instance.T):
                    if self.x[i][j][t] > self.z[i][t]:
                        print(
                            f"ERROR: for site {i}, customer {j} at period {t}, x[i][j][t] = {self.x[i][j][t]} > z[i][t] = {self.z[i][t]}"
                        )
                        return False

        # 3. check that for each period, the sum on i of the sum on j of x[i][j][t] >= n[t]
        for t in range(self.instance.T):
            sum_x = 0
            for i in range(self.instance.I):
                for j in range(self.instance.J):
                    sum_x += self.x[i][j][t]
            if sum_x < self.instance.n[t]:
                print(
                    f"ERROR: for period {t}, the sum of x[i][j][t] on i and j is {sum_x} < n[t] = {self.instance.n[t]}"
                )
                return False

        # 4. check that for each site, for each period, z[i][t] = y[i][t] + z[i][t-1] with z[i][0] = y[i][0]
        for i in range(self.instance.I):
            for t in range(self.instance.T):
                if t == 0:
                    if self.z[i][t] != self.y[i][t]:
                        print(
                            f"ERROR: for site {i} at period {t}, z[i][t] = {self.z[i][t]} != y[i][t] = {self.y[i][t]}"
                        )
                        return False
                else:
                    if self.z[i][t] != self.y[i][t] + self.z[i][t - 1]:
                        print(
                            f"ERROR: for site {i} at period {t}, z[i][t] = {self.z[i][t]} != y[i][t] + z[i][t-1] = {self.y[i][t]} + {self.z[i][t-1].x}"
                        )
                        return False

        # 5. check that for each period, the sum on i of y[i][t] = p[t]
        for t in range(self.instance.T):
            sum_y = 0
            for i in range(self.instance.I):
                sum_y += self.y[i][t]
            if sum_y != self.instance.p[t]:
                print(
                    f"ERROR: for period {t}, the sum of y[i][t] on i is {sum_y} != p[t] = {self.instance.p[t]}"
                )
                return False

        # 6. check that for each site, the sum on t of y[i][t] <= 1
        for i in range(self.instance.I):
            sum_y = 0
            for t in range(self.instance.T):
                sum_y += self.y[i][t]
            if sum_y > 1:
                print(f"ERROR: for site {i}, the sum of y[i][t] on t is {sum_y} > 1")
                return False

        # 7. check that for each customer, for each period (except the first one), the sum on i of x[i][j][t] >= x[i][j][t-1]
        for j in range(self.instance.J):
            for t in range(1, self.instance.T):
                sum_x = 0
                for i in range(self.instance.I):
                    sum_x += self.x[i][j][t]
                sum_x_prev = 0
                for i in range(self.instance.I):
                    sum_x_prev += self.x[i][j][t - 1]
                if sum_x < sum_x_prev:
                    print(
                        f"ERROR: for customer {j} at period {t}, the sum of x[i][j][t] on i is {sum_x} < the sum of x[i][j][t-1] on i = {sum_x_prev}"
                    )
                    return False

        # 8. check the objective value
        obj = 0
        for t in range(self.instance.T):
            for i in range(self.instance.I):
                obj += self.instance.f[i][t] * self.y[i][t]
                for j in range(self.instance.J):
                    obj += self.instance.c[i][j][t] * self.x[i][j][t]
        if abs(obj - self.objective_value) > 0.0001:
            print(f"ERROR: the objective value is {self.objective_value} != {obj}")
            return False

        return True

    def write(self):
        # create a _SOLUTION_DIR if it does not exist
        Path(self.__SOLUTION_DIR).mkdir(parents=True, exist_ok=True)
        _file_path = self.__SOLUTION_DIR + "/solution_" + self.instance.name + ".txt"
        with open(_file_path, "w") as file:
            # the first line is the total cost of the solution, then
            # a line for each site with the site number (starting at 1) and the period from which the site is open (0 if it is not open)
            # a line for each customer (starting at 1) and the period from which the customer is covered
            file.write(str(self.objective_value))
            sites_period = self._get_sites_period()
            for i in range(self.instance.I):
                file.write(f"\n{i + 1} {sites_period[i]}")

            customers_period = self._get_customers_period()
            for j in range(self.instance.J):
                file.write(f"\n{j + 1} {customers_period[j]}")

            file.close()

        print(f"Solution written to {_file_path}")
