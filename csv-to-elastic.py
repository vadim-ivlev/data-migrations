#!/usr/bin/env python
# coding: utf-8

# ## Export CSV files to Elasticsearch
# 
# Change input_file_name, elastic_endpoint, index_name, max_number, batch_size variables here:
# 
# To access notebook via ssh: `$ ssh -N -L 8888:localhost:8888 {user}@{server_ip}`

# In[1]:


import os
import csv
import json
import sys
import requests
from pprint import pprint


# In[3]:


username = 'admin'
password = os.getenv('RGPASS')


def save_batch(lines: list, elastic_endpoint:str, index_name:str):
    """saves batch of lines to database"""
    data = ''.join(lines)
#     print(data)
#     print('----------------------------------')
    r = requests.post(f'{elastic_endpoint}{index_name}/_bulk', 
                      headers = {'Content-Type': 'application/x-ndjson; charset=UTF-8'}, 
                      auth=(username,password),
                      data=data.encode('utf-8'))
    try:
        rjson=r.json()
        if rjson.get('errors') is not False:
            pprint(rjson)
    except:
        pprint(r)
        
    lines.clear()
    
    
def save_csv_file_to_elastic(input_file_name: str, elastic_endpoint:str, index_name:str,  max_number=0, batch_size=1000):
    """Saves CSV file to elasticsearch
    - input_file_name - name of CSV file
    - max_number - max number of records to save
    - batch_size  - number of records in a batch 
    """
    # to process long fields in CSS file
    csv.field_size_limit(sys.maxsize)
    
    
    counter =0    # aka record id 
    lines =[]     # list of text lines to save
    
    with open(input_file_name) as input_file:
        reader = csv.DictReader(input_file)

        for row in reader:
            if counter >= max_number: break
            lines.append('{ "index" : {"_id" : "'+str(counter)+'" } }\n')
            lines.append(json.dumps(row, ensure_ascii=False)+'\n')
            counter += 1
            if counter % batch_size ==0:
                print(f'counter = {counter}----------------')
                save_batch(lines, elastic_endpoint, index_name)
                
        print(f'counter = {counter}----------------')
        save_batch(lines, elastic_endpoint, index_name)


# Saving to **Ilmira** computer

# In[ ]:


get_ipython().run_cell_magic('time', '', '\n# name of CSV file\ninput_file_name = "/Volumes/ssd/dumps/articles_i.csv"\n\n# end point of Elasticsearch\nelastic_endpoint = "http://134.0.107.93:9094/elasticsearch/"\n\n# max number of records to save\nmax_number = 1210000\n\n# number of records in a batch\nbatch_size = 5000\n\n# save_csv_file_to_elastic(input_file_name, elastic_endpoint, index_name, max_number, batch_size)')


# Saving to **Azure**

# In[5]:


get_ipython().run_cell_magic('time', '', '\n# input directory\nsource_dir = "/Volumes/ssd/dumps-2020-10-09/"\n\n# Azure elastic endpoint\nazure_endpoint = "http://13.79.79.34:9094/elasticsearch/"\n\nsave_csv_file_to_elastic(source_dir+\'rubrics.csv\', azure_endpoint, \'rubrics\', 2000 , 500)')


# In[6]:


save_csv_file_to_elastic(source_dir+'rubrics_objects.csv', azure_endpoint, 'rubrics_objects', 5000000 , 10000)


# In[7]:


get_ipython().run_cell_magic('time', '', "\nsave_csv_file_to_elastic(source_dir+'articles.csv', azure_endpoint, 'articles', 1250000 , 5000)")

