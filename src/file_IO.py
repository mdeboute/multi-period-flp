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