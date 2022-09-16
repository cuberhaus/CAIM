import pandas as pd
import matplotlib.pyplot as plt
import numpy
import math
from tqdm import tqdm
from functools import reduce
from operator import concat
from scipy.optimize import curve_fit

def ZipfLaw(rank, a, b, c):
    return c /((rank + b)**a)



def plots(is_log):
    directory_path = "./"
    path_words = "data2022-09-11 00:10:05.060597.csv"
    df = pd.read_csv(path_words, sep=",", header=0)
    rank = list(range(1, 501))

    
    freq = df.iloc[0:500,0].values.tolist()
    
    #freq = df.iloc[0:500,[0]]
    #freq = reduce(concat, freq.values.tolist())
    #print(freq)
        #plt.figure(0)
    popt, pcov = curve_fit(ZipfLaw, rank, freq, bounds=([0.2, -100000.0, -100000.0],[1.8, 100000.0, 1000000.0]))
    
    plt.plot(rank, freq, label="Normal")
    plt.plot(rank, ZipfLaw(rank, *popt), label="ZipfLaw")	
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
