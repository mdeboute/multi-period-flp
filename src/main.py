import sys
from FLPData import FLPData
from FLPMIPModel import FLPMIPModel
from FLPHeuristic import FLPHeuristic


def main():
    argv = sys.argv[1:]

    if len(argv) < 2 or len(argv) > 3:
        print("Usage: python3 main.py <instance_file> <method> (<time_limit>)")
        print("Where <method> is one of: MIP or H")
        print("<time_limit> is optional, its default value is set to 600 seconds")
        exit(1)

    file_path = argv[0]
    method = argv[1]
    time_limit = 600
    if len(argv) == 3:
        time_limit = int(argv[2])

    instance = FLPData(file_path=file_path)

    if method == "MIP":
        model = FLPMIPModel(instance=instance)
        solution = model.solve(time_limit=time_limit)
        if solution.check_feasibility():
            solution.write()
        else:
            print("The solution is not feasible!")
    elif method == "H":
        model = FLPHeuristic(instance=instance)
        solution = model.solve()
        if solution.check_feasibility():
            solution.write()
        else:
            print("The solution is not feasible!")
    else:
        print("Unknown method: " + method)
        print("Available methods: MIP, H")
        exit(1)

    return 0


if __name__ == "__main__":
    main()
