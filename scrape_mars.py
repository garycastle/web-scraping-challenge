#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
from webdriver_manager.chrome import ChromeDriverManager


# In[2]:

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


# In[3]:
def scrape():
    browser = init_browser()

    browser.visit('https://redplanetscience.com/')


# In[4]:


    html = browser.html
    soup = bs(html, 'html.parser')


# In[5]:


    title_results = soup.find_all('div', class_='content_title')


# In[6]:


    p_results = soup.find_all('div', class_='article_teaser_body')
    

# In[7]:


    news_title = title_results[0].text
    news_p = p_results[0].text


# In[9]:


    browser.visit('https://spaceimages-mars.com')


# In[11]:


    image_url = 'https://spaceimages-mars.com/'
    browser.visit(image_url)

    html = browser.html
    soup = bs(html, 'html.parser')

    image = soup.find('a', target ='_blank' )['href']
    featured_image_url = f'{image_url}{image}'


# In[12]:


    tables = pd.read_html('https://galaxyfacts-mars.com')


# In[13]:


    df = tables[1]

    df.columns=['description', 'value']



# In[14]:


    mars_facts_table = [df.to_html(classes='data table table-borderless', index=False, header=False, border=0)]


# In[15]:





# In[16]:


    browser.visit('https://marshemispheres.com/')


# In[17]:


    html = browser.html
    soup = bs(html, 'html.parser')


# In[18]:


    hemi_names = []

    results = soup.find_all('div', class_="collapsible results")
    hemispheres = results[0].find_all('h3')


    for name in hemispheres:
        hemi_names.append(name.text)

    hemi_names


# In[19]:



    thumbnail_results = results[0].find_all('a')
    thumbnail_links = []

    for thumbnail in thumbnail_results:
    

        if (thumbnail.img):

            thumbnail_url = 'https://marshemispheres.com/' + thumbnail['href']
        

            thumbnail_links.append(thumbnail_url)

    thumbnail_links


# In[20]:



    full_imgs = []

    for url in thumbnail_links:
    

        browser.visit(url)
    
        html = browser.html
        soup = bs(html, 'html.parser')
    

        results = soup.find_all('img', class_='wide-image')
        relative_img_path = results[0]['src']
    

        img_link = 'https://marshemispheres.com/' + relative_img_path
    

        full_imgs.append(img_link)

    full_imgs


# In[21]:



    mars_hemi_zip = zip(hemi_names, full_imgs)

    hemisphere_image_urls = []


    for title, img in mars_hemi_zip:
    
        mars_hemi_dict = {}
    

        mars_hemi_dict['title'] = title
    

        mars_hemi_dict['img_url'] = img
    

        hemisphere_image_urls.append(mars_hemi_dict)

    hemisphere_image_urls


# In[22]:


    mars_data = {
        'news_title': news_title,
        'news_paragraph': news_p,
        'featured_image': featured_image_url,
        'mars_facts': mars_facts_table,
        'hemispheres': hemisphere_image_urls
}

    browser.quit()
# In[ ]:


    return mars_data

