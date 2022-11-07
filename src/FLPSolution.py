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
    ):
        self.instance = instance
        self.objective_value = objective_value
        self.x = x  # x[i][j][t] = the quantity of customer j (j = 0, 1, ..., J-1) served from site i (i = 0, 1, ..., I-1) at time t (t = 0, 1, ..., T-1)
        self.y = y  # y[i][t] = 1 if site i (i = 0, 1, ..., I-1) is open at time t (t = 0, 1, ..., T-1), 0 otherwise

    def __str__(self):
        return f"FLPSolution(objective_value={self.objective_value})"

    def __repr__(self):
        return self.__str__()

    def getSitesPeriod(self):
        sitesPeriod = [0 for _ in range(self.instance.I)]
        for i in range(self.instance.I):
            for t in range(self.instance.T):
                if self.y[i][t].x == 1 and sitesPeriod[i] == 0:
                    sitesPeriod[i] = t + 1
                    break
        return sitesPeriod

    def getCustomersPeriod(self):
        # we want to know from which period each customer is covered
        # example: [2, 1, 1, 2] means that customer 0 is covered from period 2, customer 1 from period 1, customer 2 from period 1 and customer 3 from period 2
        customersPeriod = [0 for _ in range(self.instance.J)]
        # TODO: implement this method
        return customersPeriod

    def write(self):
        # the first line is the total cost of the solution, then
        # a line for each site with the site number (starting at 1) and the period from which the site is open (0 if it is not open)
        # a line for each customer (starting at 1) and the period from which the customer is covered
        file_path = self.__SOLUTION_DIR + self.instance.name + "_result.txt"
        with open(file_path, "w") as file:
            file.write(str(self.objective_value))
            sitesPeriod = self.getSitesPeriod()
            for i in range(self.instance.I):
                file.write(f"\n{i + 1} {sitesPeriod[i]}")

            customersPeriod = self.getCustomersPeriod()
            for j in range(self.instance.J):
                file.write(f"\n{j + 1} {customersPeriod[j]}")

            file.close()

        print(f"Solution written to {file_path}")
