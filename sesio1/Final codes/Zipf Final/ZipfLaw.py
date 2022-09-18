import pandas as pd
import matplotlib.pyplot as plt
import numpy
import math
import argparse
import os
from tqdm import tqdm
from functools import reduce
from operator import concat
from scipy.optimize import curve_fit



def ZipfLaw(rank, a, b, c):
    return c /((rank + b)**a)

def plots(is_log):
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True, default=None, help='Path to the files')
    
    directory_path = "./"
    path_words = parser.parse_args().path
    df = pd.read_csv(path_words, sep="\t", header=0)
    rank = list(range(1, 1001))

    
    freq = df.iloc[0:1000,0].values.tolist()  
    popt, pcov = curve_fit(ZipfLaw, rank, freq, bounds=([0.5, -500000.0, -500000.0],[2.0, 500000.0, 5000000.0]))
        
    print('Zipf parameters:')
    if is_log:
        print("Log graph:")
    else: print("No log graph:")
        
    print("a = %f, b = %f, c = %f" % (popt[0],popt[1], popt[2]))
    
    plt.plot(rank, freq, label="Normal")
    plt.plot(rank, ZipfLaw(rank, *popt), label="ZipfLaw")	
    plt.legend()
    plt.ylabel('Frequency')
    plt.xlabel("Rank")

    if is_log:
        plt.loglog()
        plt.savefig(directory_path + "zipf_log " + str(os.path.splitext(path_words)[0]) + ".png")
    else:
        plt.savefig(directory_path + "zipf_no_log " + str(os.path.splitext(path_words)[0]) + ".png")
    
    plt.close()    


# No log graph
plots(False)

# Log graph
plots(True)
