#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import packages
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import pandas as pd
from tqdm import tqdm


# In[2]:


#start new chrome browser
driver = webdriver.Chrome('F:\Maged\Data Analysis\chromedriver.exe')


# In[3]:


#scraping the test page
url = 'https://webscraper.io/test-sites/e-commerce/static/computers/laptops'
driver.get(url)
driver.maximize_window()


# In[4]:


#find the caption of each product
products = driver.find_elements_by_class_name('caption')


# In[5]:


# function to get the links of the products in each page
def collect_links():
    links = []
    #find the caption of each product in the first page
    products = driver.find_elements_by_class_name('caption')
    #loop through elements to get the links for each product
    for i in products:
        links.append(i.find_elements_by_tag_name('a')[0].get_attribute('href')) 
    return links   


# In[6]:


# get the pagination last page
pages_number = int(driver.find_element_by_class_name('pagination').text.split('\n')[-2])


# In[7]:


#get the product links
product_links = []
# loop through all pages to get the links
for _ in tqdm(range(pages_number), desc = 'Getting Required Links'):
    product_links.extend(collect_links()) #extend links in one list not lists inside list
    driver.find_elements_by_class_name('page-link')[-1].click()
    driver.maximize_window()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME , 'col-md-9'))) # wait until page is loaded


# In[8]:


len(product_links)


# In[9]:


# Loading records from each link
record = []
for url in tqdm(product_links, desc ="Scraping Records"):
    driver.get(url)
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME , 'container test-site'))) # wait until page is loaded
    record.append(re.split('\n|,',driver.find_element_by_class_name('caption').text))
    driver.close


# In[10]:


#convert the records list into pandas dataframe
records = pd.DataFrame(record)


# In[11]:


print(records)


# In[ ]:




