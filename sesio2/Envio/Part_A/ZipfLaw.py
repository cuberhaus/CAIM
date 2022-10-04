import argparse
import os

import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

# Global variables
DIRECTORY_PATH = "./"


def zipf_law(rank, a, b, c):
    """
    Given a word rank and parameters a,b,c return the value in a power-law distribution
    :param rank: rank
    :param a: a
    :param b: b
    :param c: c
    :return:
    """
    return c / ((rank + b) ** a)


def plots(is_log):
    """
    Draw a plot of a given dataset to show it follows Zipf's Law
    :param is_log: if True, draw the plot in a log-log scale, otherwise draw in a 1:1 scale
    :return None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True, default=None, help='Path to the files')

    path_words = parser.parse_args().path
    df = pd.read_csv(path_words, sep="\t", header=0)
    rank = list(range(1, 1001))

    freq = df.iloc[0:1000, 0].values.tolist()
    popt, pcov = curve_fit(zipf_law, rank, freq, bounds=([0.5, -500000.0, -500000.0], [2.0, 500000.0, 5000000.0]))

    print('Zipf parameters:')
    if is_log:
        print("Log graph:")
    else:
        print("No log graph:")

    print("a = %f, b = %f, c = %f" % (popt[0], popt[1], popt[2]))

    plt.plot(rank, freq, label="Normal")
    plt.plot(rank, zipf_law(rank, *popt), label="ZipfLaw")
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
