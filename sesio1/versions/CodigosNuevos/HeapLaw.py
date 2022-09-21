import pandas as pd
import matplotlib.pyplot as plt
import numpy
import math
import os
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from elasticsearch.exceptions import NotFoundError, TransportError
from scipy.optimize import curve_fit

def heap_law(N, k, B):
    return k*(N**B)

def plots(is_log, words, diff_words,directory_path):
    popt, pcov = curve_fit(heap_law, words, diff_words, bounds=([0.0, 0.1],[1000000.0, 2.0]))
    
    plt.plot(words, diff_words,"r", label="Normal")
    plt.plot(words, heap_law(words, *popt), "b--", label="HeapLaw")
    plt.xlabel("Words")
    plt.ylabel("Different Words")
    
    print(popt)
    plt.legend()
    if is_log:
        plt.loglog()
        plt.savefig(directory_path + "zipf_log" + ".png")
    else:
        plt.savefig(directory_path + "zipf_no_log" + ".png")
"""
def count_words():
    directory = os.listdir("./groups")
    for File in directory:
        words = []
        diff_words = []
        subdir = os.listdir("./groups/"+str(File))
        for f in subdir:
            try:
                client = Elasticsearch(timeout=1000)
                voc = {}
                sc = scan(client, index=str(f).lower(), query={"query" : {"match_all": {}}})
                for s in sc:
                    try:    
                        tv = client.termvectors(index=str(f).lower(), id=s['_id'], fields=['text'])
                        if 'text' in tv['term_vectors']:
                            for t in tv['term_vectors']['text']['terms']:
                                if t in voc:
                                    voc[t] += tv['term_vectors']['text']['terms'][t]['term_freq']
                                else:
                                    voc[t] = tv['term_vectors']['text']['terms'][t]['term_freq']
                    except TransportError:
                        pass
                lpal = []

                for v in voc:
                    lpal.append((v.encode("utf-8", "ignore"), voc[v]))
            
                N = 0
                for pal, cnt in sorted(lpal, key=lambda x: x[0 if False else 1]):
                    N = N + int(cnt)
                words.append(N)
                diff_words.append(len(lpal))        
    
            except NotFoundError:
                print(f'Index {index} does not exists')    
        plots(False, words, diff_words,str(File))                                    
"""    

def count_words():
    directory = os.listdir("./groups/pg30896.txt")
    words = []
    diff_words = []
    
    for i in range(1,17):
        try:
            client = Elasticsearch(timeout=1000)
            voc = {}
            sc = scan(client, index=(str(i)+"pg30896.txt").lower(), query={"query" : {"match_all": {}}})
            for s in sc:
                try:    
                    tv = client.termvectors((str(i)+"pg30896.txt").lower(), id=s['_id'], fields=['text'])
                    if 'text' in tv['term_vectors']:
                        for t in tv['term_vectors']['text']['terms']:
                            if t in voc:
                                voc[t] += tv['term_vectors']['text']['terms'][t]['term_freq']
                            else:
                                voc[t] = tv['term_vectors']['text']['terms'][t]['term_freq']
                except TransportError:
                    pass
            lpal = []

            for v in voc:
                lpal.append((v.encode("utf-8", "ignore"), voc[v]))
        
            N = 0
            for pal, cnt in sorted(lpal, key=lambda x: x[0 if False else 1]):
                N = N + int(cnt)
            words.append(N)
            print(N)
            diff_words.append(len(lpal))        

        except NotFoundError:
            print(f'Index {index} does not exists')    
    plots(False, words, diff_words,"./groups/pg30896.txt")

count_words()


