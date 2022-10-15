"""
.. module:: SearchIndexWeight

SearchIndex
*************

:Description: SearchIndexWeight

    Performs a AND query for a list of words (--query) in the documents of an index (--index)
    You can use word^number to change the importance of a word in the match

    --nhits changes the number of documents to retrieve

:Authors: bejar
    

:Version: 

:Created on: 04/07/2017 10:56 

"""

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

import argparse

from elasticsearch.client import CatClient
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q

import numpy as np

__author__ = 'bejar'

nrounds = 5
alpha = 0.1
beta = 0.1
R = 1


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


def doc_count(client, index):
    """
    Returns the number of documents in an index

    :param client:
    :param index:
    :return:
    """
    return int(CatClient(client).count(index=[index], format='json')[0]['count'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, help='Index to search')
    parser.add_argument('--nhits', default=10, type=int, help='Number of hits to return')
    parser.add_argument('--query', default=None, nargs=argparse.REMAINDER, help='List of words to search')

    args = parser.parse_args()

    index = args.index
    query = args.query
    print(query)
    nhits = args.nhits

    try:
        client = Elasticsearch()
        s = Search(using=client, index=index)

        if query is not None:
            for i in range(0, nrounds):
                q = Q('query_string', query=query[0])
                for i in range(1, len(query)):
                    q &= Q('query_string', query=query[i])

                s = s.query(q)
                response = s[0:nhits].execute()

                # Query to dictionary		
                dictionary = {}
                for element in query:
                    if '^' in element:
                        key, value = element.split('^')
                        value = float(value)
                    else:
                        key = element
                        value = 1.0
                    dictionary[key] = value

                print(dictionary)

                sum_documents = 0
                # For every document compute TF-IDF				
                for r in response:  # only returns a specific number of results
                    tfidf = toTFIDF(client, index, r.meta.id)
                    for e in range(len(tfidf)):
                        sum_documents += tfidf[e][1]
                    print(f'ID= {r.meta.id} SCORE={r.meta.score}')
                    print(f'PATH= {r.path}')
                    print(f'TEXT: {r.text[:50]}')
                    print('-----------------------------------------------------------------')

                # Create new query
                new_dictionary = dictionary
                second_part = beta * sum_documents / nhits
                for e in dictionary:
                    new_dictionary[e] = alpha * new_dictionary[e] + second_part

                query = []
                for element in new_dictionary:
                    query.append(element + '^' + str(new_dictionary[element]))

                print(query)

        else:
            print('No query parameters passed')

        print(f"{response.hits.total['value']} Documents")

    except NotFoundError:
        print(f'Index {index} does not exists')
