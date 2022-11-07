from FLPSolution import FLPSolution
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SOLUTION_DIR = str(BASE_DIR) + "/solution/"


def parse(file_path: str):
    with open(file_path, "r") as file:
        # First line: I J T
        I, J, T = [int(x) for x in file.readline().split()]

        # Second line: values of p for t = 0, 1, ..., T-1
        p = [int(x) for x in file.readline().split()]

        # Third line: values of n for t = 0, 1, ..., T-1
        n = [int(x) for x in file.readline().split()]

        # From fourth line: a block of lines for every i = 0, 1, ..., I-1
        f = [[0 for _ in range(T)] for _ in range(I)]
        c = [[[0 for _ in range(T)] for _ in range(J)] for _ in range(I)]

        for i in range(I):
            # First line of each block: values of f for t = 0, 1, ..., T-1
            f[i] = [int(x) for x in file.readline().split()]

            # Then, a line for every j: values of c for t = 0, 1, ..., T-1
            for j in range(J):
                c[i][j] = [int(x) for x in file.readline().split()]

        return I, J, T, n, p, f, c


def write(instance_name: str, solution: FLPSolution):
    # the first line is the total cost of the solution, then
    # a line for each site with the site number (starting at 1) and the period from which the site is open (0 if it is not open)
    # a line for each customer (starting at 1) and the period from which the customer is covered

    file_path = SOLUTION_DIR + instance_name + "_result.txt"
    with open(file_path, "w") as file:
        file.write(str(int(solution.objective_value)))
        sitesPeriod = solution.getSitesPeriod()
        for i in range(solution.instance.I):
            file.write(f"\n{i + 1} {sitesPeriod[i]}")

        customersPeriod = solution.getCustomersPeriod()
        for j in range(solution.instance.J):
            file.write(f"\n{j + 1} {customersPeriod[j]}")

        file.close()

    print(f"Solution written to {file_path}")
