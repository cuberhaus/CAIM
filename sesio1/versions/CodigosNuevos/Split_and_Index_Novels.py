import os
import shutil
import codecs
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl import Index

def create_groups():
	if os.path.exists("./groups"):
		shutil.rmtree("./groups") 
	os.mkdir("./groups")
	directory = os.listdir("./novels")
	for f in directory:
		File = open("./novels/"+str(f), "r")
		text = File.readlines()
		size = len(text)//16
		os.mkdir("./groups/" + str(f))
		for i in range(1, 17):
			output = open(os.path.join("./groups/"+str(f), str(i)), "w")
			for l in text[:(i*size+size)]:
				output.write(l)
			output.close()	
	

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
"""
def create_indexes():
	
	directory = os.listdir("./groups")
	for Dir in directory:
	    ldocs = []
	    for i in range(1,17):
		    ftxt = codecs.open("./groups/"+str(Dir)+"/"+str(i), "r", encoding='iso-8859-1')
		    text = ''
		    for line in ftxt:
		    	text += line
            # Insert operation for a document with fields' path' and 'text'
		    ldocs.append({'_op_type': 'index', '_index': (str(i)+str(Dir)).lower(), 'path': "./groups/"+str(Dir)+"/"+str(i), 'text': text})
	
		    # Working with ElasticSearch
		    client = Elasticsearch(timeout=1000)
		    try:
            	# Drop index if it exists
		    	ind = Index((str(i)+str(Dir)).lower(), using=client)
		    	ind.delete()
		    except NotFoundError:
		    		pass
    	    # then create it
		    ind.settings(number_of_shards=1)
		    ind.create()

    	    # Bulk execution of elasticsearch operations (faster than executing all one by one)
		    print('Indexing ...')
		    bulk(client, ldocs)
"""
def create_indexes():
    Dir = "pg30896.txt"
    ldocs = []
    for i in range(1,17):
	    ftxt = codecs.open("./groups/"+str(Dir)+"/"+str(i), "r", encoding='iso-8859-1')
	    text = ''
	    for line in ftxt:
	    	text += line
        # Insert operation for a document with fields' path' and 'text'
	    ldocs.append({'_op_type': 'index', '_index': (str(i)+str(Dir)).lower(), 'path': "./groups/"+str(Dir)+"/"+str(i), 'text': text})

	    # Working with ElasticSearch
	    client = Elasticsearch(timeout=1000)
	    try:
        	# Drop index if it exists
	    	ind = Index((str(i)+str(Dir)).lower(), using=client)
	    	ind.delete()
	    except NotFoundError:
	    		pass
	    # then create it
	    ind.settings(number_of_shards=1)
	    ind.create()

	    # Bulk execution of elasticsearch operations (faster than executing all one by one)
	    print('Indexing ...')
	    bulk(client, ldocs)
	    

create_groups()
create_indexes()


