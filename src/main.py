import sys
from file_IO import parse
from FLPData import FLPData


def main():
    argv = sys.argv[1:]

    if len(argv) != 1:
        print("Usage: python main.py <instance_file>")
        return 1

    filePath = argv[0]

    I, J, T, n, p, f, c = parse(filePath)

    instance = FLPData(I, J, T, n, p, f, c)

    print(instance)

    return 0


if __name__ == "__main__":
    main()
