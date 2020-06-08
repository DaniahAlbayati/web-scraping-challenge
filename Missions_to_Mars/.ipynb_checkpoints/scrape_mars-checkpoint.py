#!/usr/bin/env python
# coding: utf-8




from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def scrape_all():

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url ='https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    dic={}

    #Scrape the [NASA Mars News Site](https://mars.nasa.gov/news/) and collect the latest News Title
    #and Paragraph Text. Assign the text to variables that you can reference later.
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    title= soup.find_all('div', class_='content_title')
    body= soup.find('div', class_='article_teaser_body')
    print(title[1].text)
    print(body.text)

    news_title=title[1].text
    news_p= body.text

    dic[news_title]=news_title
    dic[news_p]=news_p

    dic

    #browser.quit()
    # JPL Mars Space Images - Featured Image
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    browser.find_by_id('full_image').click()
    browser.find_link_by_partial_text('more info').click()

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    imgs=soup.find('figure', class_='lede')
    print(imgs)
    print(imgs.a)
    print(imgs.a.img)
    print(imgs.a.img['src'])

    featured_image_url='https://www.jpl.nasa.gov'+imgs.a.img['src']
    print(featured_image_url)
    dic[featured_image_url]=featured_image_url
    dic

    # Mars Facts
    url ='https://space-facts.com/mars/'
    facts=pd.read_html(url)
    facts
    type(facts)

    df=facts[0]
    df.columns=['Profile','Values']
    df.set_index('Profile', inplace=True)
    df.head()

    html_facts = df.to_html()
    html_facts
    

    #strip unwanted newlines to clean up the table.
    html_facts.replace('\n', '')

    df.to_html('facts.html')

    #Mars Hemispheres
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    image_urls= []
    imgs = browser.find_by_css("a.product-item h3")
    imgs

    # For loop

    for i in range(len(imgs)):
        hemisphere = {}   
        browser.find_by_css("a.product-item h3")[i].click()
        
        # Find Sample Image
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        # Get the Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # Append
        image_urls.append(hemisphere)
        
        # find imgs back
        browser.back()
    image_urls

    dic['hemisphere']=image_urls
    dic

    return dic
if __name__ == "__main__":
    print(scrape_all())