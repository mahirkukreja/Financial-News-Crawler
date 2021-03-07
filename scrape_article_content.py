#!/usr/bin/env python
# coding: utf-8

# In[1]:


##Imports
import pandas as pd
import time
from tqdm.notebook import tqdm
import os
import json
from multiprocessing import Pool
import urllib
from bs4 import BeautifulSoup
import requests
from lxml import html
import re
from pandas.core.common import flatten
from sklearn.utils import shuffle
from fake_useragent import UserAgent


# In[2]:


## Scrape article content from Links
def scrape_content(url):
    try:
        ua = UserAgent()
        userAgent = ua.random
        headers = {'User-Agent': userAgent}
        soup = BeautifulSoup(requests.get(url,headers=headers).text, 'html.parser')
        time.sleep(3)
        whole_section = soup.find('div',{'class':'content_wrapper arti-flow'})
        content = whole_section.findAll('p')
        title = soup.find('h1',{'class':'article_title artTitle'}).text
        desc = soup.find('h2',{'class':'article_desc'}).text
        paragraphs=[]
        for i in content:
            paragraphs.append(i.text)
        paragraphs="\n".join(paragraphs)
        df=pd.DataFrame()
        df['title']=[title]
        df['desc']=[desc]
        df['content']=[paragraphs]
        df.to_csv('financial_news.csv', mode='a', index=False, header=False)
        return 'Done'
    except Exception as e:
        return e


# In[3]:


## Main Function
if __name__ == '__main__':
    start=time.time()
    links=pd.read_csv('links.csv')
    link_list=list(links['Links'])
    articles=pd.DataFrame(columns=['title','desc','content'])
    articles.to_csv('financial_news.csv',index=False)
    pool = Pool(20)                       
    content=pool.map(scrape_content,[i for i in link_list])
    end=time.time()
    print(end-start)
    pool.close()

