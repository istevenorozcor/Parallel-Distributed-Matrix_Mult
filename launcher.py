from argparse import ArgumentParser
from os import popen

from pandas import DataFrame
from tqdm import trange


def single_experiment(matrix_size, threads):
    data = []
    executables = ("MM1c", "MM1r")
    algorithms = ("row-column", "row-row")
    for executable, algorithm in zip(executables, algorithms):
        stream = popen(f"./{executable} {matrix_size} {threads} 0")
        for line in stream.readlines():
            values = line.strip().split(",")
            values.append(algorithm)
            data.append(values)
    return data


def all_experiments(matrix_sizes, threads, repetitions):
    data = []
    for matrix_size in matrix_sizes:
        for thread in threads:
            for _ in trange(
                repetitions,
                desc=f"Size: {matrix_size}, {thread} threads",
                unit="exec",
            ):
                data.extend(single_experiment(matrix_size, thread))
    return data


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Run matrix multiplication experiments and save data as CSV.",
        epilog="The output of this program should be used with graphics.py",
    )
    parser.add_argument(
        "output_file",
        help="CSV file where the results will be saved",
    )
    args = parser.parse_args()

    matrix_sizes = range(200, 2001, 200)
    threads = range(2, 21, 2)
    repetitions = 30

    data = all_experiments(matrix_sizes, threads, repetitions)
    columns = ["Matrix_Size", "N_Threads", "Thread", "Time", "Algorithm"]
    data = DataFrame(data, columns=columns)
    data.to_csv(args.output_file, index=False)
