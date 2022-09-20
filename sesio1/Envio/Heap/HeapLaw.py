import os

import matplotlib.pyplot as plt
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError, TransportError
from elasticsearch.helpers import scan
from scipy.optimize import curve_fit


def heap_law(N, k, B):
    """
    Given N the number of total words and parameters k,B return the value,
    that corresponds to the power-law distribution.
    :param N: N numbers
    :param k: k
    :param B: B
    :return:
    """
    return k * (N ** B)


def plots(is_log, words, diff_words, directory_path):
    """
    Draw a plot of a given dataset to show it follows Heap's Law
    :param is_log: if True, draw the plot in a log-log scale, otherwise draw in a 1:1 scale
    :param words: all words
    :param diff_words: different words
    :param directory_path: path to store the file
    :return:
    """
    popt, pcov = curve_fit(heap_law, words, diff_words, bounds=([0.0, 0.1], [1000000.0, 2.0]))

    print('Heap parameters:')
    if is_log:
        print("Log graph:")
    else:
        print("No log graph:")

    print("k = %f, B = %f" % (popt[0], popt[1]))

    plt.plot(words, diff_words, "r", label="Normal")
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
    directory = os.listdir("./groups")
    words = []
    diff_words = []
    for i in directory:
        try:
            index = str(i)
            print(index)
            client = Elasticsearch(timeout=1000)
            voc = {}
            sc = scan(client, index=index, query={"query": {"match_all": {}}})
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

            lpal = []
            N = 0
            diff_counter = 0
            for v in voc:
                lpal.append((v.encode("utf-8", "ignore"), voc[v]))

            for pal, cnt in sorted(lpal, key=lambda x: x[0 if False else 1]):
                if (pal.decode()).isalpha():
                    diff_counter = diff_counter + 1
                    N = N + int(cnt)

            words.append(N)
            diff_words.append(diff_counter)
        except NotFoundError:
            print(f'Index {index} does not exists')

    print(words)
    print(diff_words)
    plots(False, words, diff_words, "./")
    plots(True, words, diff_words, "./")


count_words()
