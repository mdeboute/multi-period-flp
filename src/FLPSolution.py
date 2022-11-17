from FLPData import FLPData
from pathlib import Path


class FLPSolution:
    __BASE_DIR = Path(__file__).resolve().parent.parent
    __SOLUTION_DIR = str(__BASE_DIR) + "/solution/"

    def __init__(
        self,
        instance: FLPData,
        objective_value: int,
        x: list([list([list()])]),
        y: list([list()]),
        z: list([list()]),
    ):
        self.instance = instance
        self.objective_value = objective_value
        self.x = x  # x[i][j][t] = 1 if we affect the customer j (j = 0, 1, ..., J-1) to the site i (i = 0, 1, ..., I-1) at time t (t = 0, 1, ..., T-1), 0 otherwise
        self.y = y  # y[i][t] = 1 if we open site i (i = 0, 1, ..., I-1) at time t (t = 0, 1, ..., T-1), 0 otherwise
        self.z = z  # z[i][t] = 1 if site i (i = 0, 1, ..., I-1) is open at time t (t = 0, 1, ..., T-1), 0 otherwise

    def __str__(self):
        return f"FLPSolution(objective_value={self.objective_value})"

    def __repr__(self):
        return self.__str__()

    def __get_sites_period__(self):
        # we want to know from which period each site is open
        # example: [2, 1, 1, 2] means that site 0 is open from period 2, site 1 from period 1, site 2 from period 1 and site 3 from period 2
        sites_period = [0 for _ in range(self.instance.I)]
        for i in range(self.instance.I):
            for t in range(self.instance.T):
                if self.z[i][t].x == 1 and sites_period[i] == 0:
                    sites_period[i] = t + 1
                    break
        return sites_period

    def __get_customers_period__(self):
        # we want to know from which period each customer is covered
        # example: [2, 1, 1, 2] means that customer 0 is covered from period 2, customer 1 from period 1, customer 2 from period 1 and customer 3 from period 2
        customers_period = [0 for _ in range(self.instance.J)]
        for j in range(self.instance.J):
            for t in range(self.instance.T):
                for i in range(self.instance.I):
                    if self.x[i][j][t].x == 1 and customers_period[j] == 0:
                        customers_period[j] = t + 1
                        break
        return customers_period

    def write(self):
        # create a __SOLUTION_DIR if it does not exist
        Path(self.__SOLUTION_DIR).mkdir(parents=True, exist_ok=True)
        file_path = self.__SOLUTION_DIR + self.instance.name + "_result.txt"
        with open(file_path, "w") as file:
            # the first line is the total cost of the solution, then
            # a line for each site with the site number (starting at 1) and the period from which the site is open (0 if it is not open)
            # a line for each customer (starting at 1) and the period from which the customer is covered
            file.write(str(self.objective_value))
            sites_period = self.__get_sites_period__()
            for i in range(self.instance.I):
                file.write(f"\n{i + 1} {sites_period[i]}")

            customers_period = self.__get_customers_period__()
            for j in range(self.instance.J):
                file.write(f"\n{j + 1} {customers_period[j]}")

            file.close()

        print(f"Solution written to {file_path}")
