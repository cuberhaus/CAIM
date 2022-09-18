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
    popt, pcov = curve_fit(heap_law, words, diff_words)
    
    print('Heap parameters:')
    if is_log:
        print("Log graph:")
    else: print("No log graph:")
        
    print("k = %f, B = %f" % (popt[0],popt[1]))
        
    plt.plot(words, diff_words,"r", label="Normal")
    plt.plot(words, heap_law(words, *popt), "b--", label="HeapLaw")
    plt.xlabel("Words")
    plt.ylabel("Different Words")
    
    plt.legend()
    if is_log:
        plt.loglog()
        plt.savefig(directory_path + "heap_log" + ".png")
    else:
        plt.savefig(directory_path + "heap_no_log" + ".png")
    plt.close()




def count_words():
    directory = os.listdir("./novels")
    
    files = []
    for f in directory:
	    File = open("./novels/"+str(f), "r")
	    text = File.readlines()
	    files.append([len(text), str(f)])
	
    files.sort()
    n_groups = len(files)//3
    size_group= len(files)//n_groups
    
    for i in range(0, n_groups):
        words = []
        diff_words = []
        lpal = []
        N = 0
        for j in range(0,size_group):                       
            try:
                index = str(os.path.splitext(files[i*size_group+j][1])[0]).lower()
                print(index)
                client = Elasticsearch(timeout=1000)
                voc = {}
                sc = scan(client, index=index, query={"query" : {"match_all": {}}})
                for s in sc:
                    try:    
                        tv = client.termvectors(index=index, id=s['_id'], fields=['text'])
                        if 'text' in tv['term_vectors']:
                            for t in tv['term_vectors']['text']['terms']:
                                if t in voc:
                                    voc[t] += tv['term_vectors']['text']['terms'][t]['term_freq']
                                else:
                                    voc[t] = tv['term_vectors']['text']['terms'][t]['term_freq']
                    except TransportError:
                        pass
                
                
                for v in voc:
                    lpal.append((v.encode("utf-8", "ignore"), voc[v]))
            
                
                for pal, cnt in sorted(lpal, key=lambda x: x[0 if False else 1]):
                        N = N + int(cnt)
                words.append(N)
                diff_words.append(len(lpal))            
            except NotFoundError:
                    print(f'Index {index} does not exists')    
     
    plots(False, words, diff_words,"./")
    plots(True, words, diff_words,"./")                                     

count_words()
