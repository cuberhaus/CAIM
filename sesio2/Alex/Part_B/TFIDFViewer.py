"""
.. module:: TFIDFViewer

TFIDFViewer
******

:Description: TFIDFViewer

    Receives two paths of files to compare (the paths have to be the ones used when indexing the files)

:Authors:
    bejar

:Version: 

:Date:  05/07/2017
"""
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from elasticsearch.client import CatClient
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q

import argparse
import os
import numpy as np

__author__ = 'bejar'


def search_file_by_path(client, index, path):
    """
    Search for a file using its path

    :param path:
    :return:
    """
    s = Search(using=client, index=index)
    q = Q('match', path=path)  # exact search in the path field
    s = s.query(q)
    result = s.execute()

    lfiles = [r for r in result]
    if len(lfiles) == 0:
        raise NameError(f'File [{path}] not found')
    else:
        return lfiles[0].meta.id


def document_term_vector(client, index, id):
    """
    Returns the term vector of a document and its statistics a two sorted list of pairs (word, count)
    The first one is the frequency of the term in the document, the second one is the number of documents
    that contain the term

    :param client:
    :param index:
    :param id:
    :return:
    """
    termvector = client.termvectors(index=index, id=id, fields=['text'],
                                    positions=False, term_statistics=True)

    file_td = {}
    file_df = {}

    if 'text' in termvector['term_vectors']:
        for t in termvector['term_vectors']['text']['terms']:
            file_td[t] = termvector['term_vectors']['text']['terms'][t]['term_freq']
            file_df[t] = termvector['term_vectors']['text']['terms'][t]['doc_freq']
    return sorted(file_td.items()), sorted(file_df.items())


def toTFIDF(client, index, file_id):
    """
    Returns the term weights of a document

    :param file:
    :return:
    """

    # Get the frequency of the term in the document, and the number of documents
    # that contain the term
    file_tv, file_df = document_term_vector(client, index, file_id)

    max_freq = max([f for _, f in file_tv])

    dcount = doc_count(client, index)

    tfidfw = []
    for (t, w), (_, df) in zip(file_tv, file_df):
        tf = w / max_freq
        idf = np.log2(dcount / df)
        tfidfw.append((t, tf * idf))
        pass
    # normalize(tfidfw)
    return tfidfw


def print_term_weigth_vector(twv):
    """
    Prints the term vector and the correspondig weights
    :param twv:
    :return:
    """
    for (term, weight) in twv:
        print(term)
        print(weight)
    return None


def normalize(tw):
    """
    Normalizes the weights in t so that they form a unit-length vector
    It is assumed that not all weights are 0
    :param tw:
    :return:
    """
    sum = 0
    for (i, j) in tw:
        # print(i, j)
        sum += j ** 2
    vmod = np.sqrt(sum)
    for i in range(len(tw)):
        tw[i] = (tw[i][0], tw[i][1] / vmod)
    return None


def cosine_similarity(tw1, tw2):
    """
    Computes the cosine similarity between two weight vectors, terms are alphabetically ordered
    :param tw1:
    :param tw2:
    :return:
    """
    #normalize(tw1)
    #normalize(tw2)
    i = 0
    j = 0
    size_tw1 = len(tw1)
    size_tw2 = len(tw2)
    summ = 0
    while i < size_tw1 and j < size_tw2:   
                                                            
        (term1,weight1) = tw1[i]    
        (term2,weight2) = tw2[j]
        if term1 == term2:   
            summ += weight1 * weight2
            i += 1
            j += 1
        elif term1 < term2:   
            i += 1
        else:   
            j += 1
            
    sum1 = 0
    for i in range(size_tw1):
        sum1 += tw1[i][1] ** 2
    sum2 = 0
    for i in range(size_tw2):
        sum2 += tw2[i][1] ** 2
    l1 = np.sqrt(sum1)
    l2 = np.sqrt(sum2)
    #print("module1: " + str(l1) + " module2: " + str(l2))
    res = summ / (l1 * l2)
    return res


def doc_count(client, index):
    """
    Returns the number of documents in an index

    :param client:
    :param index:
    :return:
    """
    return int(CatClient(client).count(index=[index], format='json')[0]['count'])


def generate_files_list(path):
    """
    Generates a list of all the files inside a path (recursivelly)
    :param path:
    :return:
    """
    if path[-1] == '/':
        path = path[:-1]

    lfiles = []
    
    for lf in os.walk(path):
        if lf[2]:
            for f in lf[2]:
                lfiles.append(lf[0] + '/' + f)
    return lfiles

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, required=True, help='Index to search')
    #parser.add_argument('--files', default=None, required=True, nargs=2, help='Paths of the files to compare')
    parser.add_argument('--path', default=False, required=True, help='Path to the files')
    parser.add_argument('--print', default=False, action='store_true', help='Print TFIDF vectors')

    args = parser.parse_args()

    index = args.index

    path = args.path
    
    directory = os.listdir(path)
    sizeFolder = len(directory)
    for i in range(0, sizeFolder):
        file1 = generate_files_list(str(path) + '/' + str(directory[i]))       
        size_file1 = len(file1)
        
        for j in range(i+1, sizeFolder):     	
            file2 = generate_files_list(str(path) + '/' + str(directory[j]))
            print("Folders: " + str(directory[i]) + "  " + str(directory[j]) + ':')
            size_file2 = len(file2)
            summ = 0
            for l in range(0, 50):
            	for t in range(0, 50):
            	    client = Elasticsearch(timeout=1000)
            	    try:
                        # Get the files ids
                        file1_id = search_file_by_path(client, index, file1[l])
                        file2_id = search_file_by_path(client, index, file2[t])

                        # Compute the TF-IDF vectors
                        file1_tw = toTFIDF(client, index, file1_id)
                        file2_tw = toTFIDF(client, index, file2_id)

                        if args.print:
	                        print(f'TFIDF FILE {file1}')
	                        print_term_weigth_vector(file1_tw)
	                        print('---------------------')
	                        print(f'TFIDF FILE {file2}')
	                        print_term_weigth_vector(file2_tw)
	                        print('---------------------')
                        sim =cosine_similarity(file1_tw, file2_tw)                  
                        print(f"Similarity = {sim}")
                        summ += sim
            	    except NotFoundError:
            	    	print(f'Index {index} does not exists')
        media = summ/2500
        print(media)


