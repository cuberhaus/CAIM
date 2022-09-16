import pandas as pd
import matplotlib.pyplot as plt
import numpy
import math
from tqdm import tqdm
from functools import reduce
from operator import concat
from scipy.optimize import curve_fit
def ZipfLaw(rank, a, b, c):
    return c / (rank + b)**a

def plots(is_log):
    directory_path = "./"
    path_words = "./data2022-09-10 12:58:02.519069_by_rank.csv"
    df = pd.read_csv(path_words, sep=",", header=0)
    #print(df)
    rank = list(range(1, 501))

    cont = 0
    freq = []
    for index, row in df.iterrows():
        for i in row:
            cont += 1
            freq.append(i)
            if cont >= 2:
                break
        if cont >= 2:
            break
    print(freq)

    #freq = df.iloc[0:500,[0]]
    #freq = reduce(concat, freq.values.tolist())
    #print(freq)
        #plt.figure(0)
    popt, pcov = curve_fit(ZipfLaw, rank, freq)
    plt.plot(rank, freq, label="1")
    plt.plot(rank, ZipfLaw(rank, *popt), label="2")
    plt.legend()
    plt.ylabel('Frequency')
    plt.xlabel("Rank")

    #if not os.path.isdir(directory_path + directory):
    #    os.makedirs(directory_path + directory)
    #plt.legend()
    if is_log:
        plt.loglog()
        plt.savefig(directory_path + "zipf_log" + ".png")
    else:
        plt.savefig(directory_path + "zipf_no_log" + ".png")



plots(False)

