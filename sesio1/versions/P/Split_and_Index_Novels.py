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
	files = []
	for f in directory:
	    size = os.path.getsize("./novels/"+str(f))
	    files.append([size, str(f)])
	
	files.sort()
				
	n_groups = len(files)//11
	size_group= len(files)//n_groups
	for k in range(0, n_groups):
		os.mkdir("./groups/" + str(k))	
		
		for i in range(0,size_group):
			output = open(os.path.join("./groups/"+str(k), str(i)+str(k)), "a")
			File = open("./novels/"+str(files[k*size_group+i][1]), "r")
			text = File.readlines()	
			
			for l in text[:len(text)]:
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

			
def create_indexes():
	
    directory = os.listdir("./groups")
    ldocs = []
    for Dir in directory:
        Folder = "./groups/"+ str(Dir)
        lfiles = generate_files_list(Folder)
        index = str(Dir)
        print(index)
        print(lfiles)
        for f in lfiles:
            print (f)
            ftxt = codecs.open(f, "r", encoding='iso-8859-1')
            
            text = ''
            for line in ftxt:
                text += line
            # Insert operation for a document with fields' path' and 'text'
            ldocs.append({'_op_type': 'index', '_index': index, 'path': f, 'text': text})

        
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
create_groups()
create_indexes()
