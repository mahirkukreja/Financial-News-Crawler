#!/usr/bin/env python
# coding: utf-8

# In[1]:


##Imports
from tqdm.notebook import tqdm
import os
import json
import pandas as pd
import time
from multiprocessing import Pool
import urllib
import requests
from lxml import html
import re
from pandas.core.common import flatten
from fake_useragent import UserAgent


# In[2]:


## Function for Crawling Article links from a Page
def get_links(pageno):
    try:
        time.sleep(5)
        ua = UserAgent()
        userAgent = ua.random
        headers = {'User-Agent': userAgent}
        page = requests.get('https://www.moneycontrol.com/news/news-all/page-'+str(pageno)+'/',headers=headers)
        html_content = html.fromstring(page.content)
        links=html_content.xpath('/html/body/section/div/ul/li/h2/a/@href')
        links_df=pd.DataFrame()
        links_df['Links']=list(flatten(links))
        links_df.to_csv('links.csv', mode='a', index=False, header=False)
        return 'Done'
    except Exception as e:
        return e


# In[3]:


## Main Function
if __name__ == '__main__':
    num_pages=int(input('How many pages would you like to crawl? '))
    num_processes=int(input('How many pool processes can you run? '))
    start=time.time()
    links=pd.DataFrame(columns=['Links'])
    links.to_csv('links.csv',index=False)
    pool = Pool(num_processes)                    
    response=pool.map(get_links, [i for i in range(1,num_pages+1)])
    end=time.time()
    print(end-start)
    pool.close()

