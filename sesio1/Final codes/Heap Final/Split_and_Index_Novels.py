import os
import shutil
import codecs
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl import Index

def create_indexes():
    directory = os.listdir("./novels")
    ldocs = []
    for File in directory:
        index = str(os.path.splitext(File)[0]).lower()
        print(index)
        ftxt = codecs.open("./novels/"+str(File), "r", encoding='iso-8859-1')
        text = ''
        for line in ftxt:
            text += line
    # Insert operation for a document with fields' path' and 'text'
        ldocs.append({'_op_type': 'index', '_index': index, 'path': "./novels/"+str(File), 'text': text})

        # Working with ElasticSearch
        client = Elasticsearch(timeout=1000)
        try:
	    # Drop index if it exists
	        ind = Index(index, using=client)
	        ind.delete()
        except NotFoundError:
	        pass
    # then create it
        ind.settings(number_of_shards=1)
        ind.create()
    # Bulk execution of elasticsearch operations (faster than executing all one by one)
        print('Indexing ...')
        bulk(client, ldocs)


create_indexes()
