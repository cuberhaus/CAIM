import argparse
import os

import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

# Global variables
DIRECTORY_PATH = "./"


def ZipfLaw(rank, a, b, c):
    """

    :param rank:
    :param a:
    :param b:
    :param c:
    :return:
    """
    return c / ((rank + b) ** a)


def plots(is_log):
    """

    :param is_log:
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True, default=None, help='Path to the files')

    path_words = parser.parse_args().path
    df = pd.read_csv(path_words, sep="\t", header=0)
    rank = list(range(1, 1001))

    freq = df.iloc[0:1000, 0].values.tolist()
    popt, pcov = curve_fit(ZipfLaw, rank, freq, bounds=([0.5, -500000.0, -500000.0], [2.0, 500000.0, 5000000.0]))

    print('Zipf parameters:')
    if is_log:
        print("Log graph:")
    else:
        print("No log graph:")

    print("a = %f, b = %f, c = %f" % (popt[0], popt[1], popt[2]))

    plt.plot(rank, freq, label="Normal")
    plt.plot(rank, ZipfLaw(rank, *popt), label="ZipfLaw")
    plt.legend()
    plt.ylabel('Frequency')
    plt.xlabel("Rank")

    if is_log:
        plt.loglog()
        plt.savefig(DIRECTORY_PATH + "zipf_log " + str(os.path.splitext(path_words)[0]) + ".png")
    else:
        plt.savefig(DIRECTORY_PATH + "zipf_no_log " + str(os.path.splitext(path_words)[0]) + ".png")

    plt.close()


def main():
    # No log graph
    plots(False)

    # Log graph
    plots(True)


if __name__ == '__main__':
    main()
