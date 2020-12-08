# Import Libaries
from bs4 import BeautifulSoup as bs
import requests
import os
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import json

def marsNews():

    # Retrieve page with requests module
    response_news = requests.get(news_url)

    # Create a Beautiful Soup Object
    soup_news = bs(response_news.text, "html.parser")

    # Set the article title variable to "news_title"
    # Article title located in div class = "content_title"
    news_title = soup_news.find('div', class_ = "content_title").text

    # Set the article's paragraph to news_p
    # Article Paragraph located in div class = "rollover_description_inner"
    news_p = soup_news.find('div', class_ = "rollover_description_inner").text

    news_dict = {"News_Title" : news_title, "News_Paragraph" : news_p}

    return news_dict

def marsImages():

    # Set up Splinter instance
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit the specific URL
    browser.visit(image_url)

    # Navigate through the website
    try:
        browser.click_link_by_id("full_image")
        browser.click_link_by_partial_href("details")
    
    except:
        print("404 Error")

    # Get the URL of the image
    html_image = browser.html
    soup_image = bs(html_image, "html.parser")

    article = soup_image.find("figure", class_ = "lede")
    link = article.find('a')
    href = link['href']

    # Merge the base url and the href url into the "featured_image_url" variable
    featured_image_url = "https://www.jpl.nasa.gov/" + href

    # Close the browser when done scraping
    browser.quit()

    # Return image url
    return featured_image_url

def marsFacts():
    # Use Pandas to scrape the Mars facts table
    tables = pd.read_html(facts_url)

    # Isolate the Mars table from the comparison table
    mars_df = tables[0]

    # Change the name of the columns
    mars_df.columns = ["Descriptors", "Facts"]

    # Convert the Dataframe to an HTML string
    mars_htmlString = mars_df.to_html()

    return mars_htmlString

def marsHemispheres():
    # Setup the Splinter Instance
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless = False)

    # Initialize a list that will hold a dictionary for each hemisphere
    hemisphere_image_urls = []

    # Go to the Hemisphere URL
    browser.visit(hemisphere_url)

    # Create a list of the hemispheres to help with loop
    hemispheres = ["Cerberus", "Schiaparelli", "Syrtis", "Valles"]

    # loop through each of the four hemispheres and extract the image url and the title
    for hemisphere in hemispheres:
        try:
            # Go to the main site
            browser.visit(hemisphere_url)
            
            # Go to the next hemisphere
            browser.click_link_by_partial_text(hemisphere)
            
            # Parse HTML with Beautiful Soup
            html = browser.html
            soup = bs(html, "html.parser")
            
            # Save the title for the hemisphere
            title = soup.find("h2", class_ = "title").text
            
            # Save the img URL
            article = soup.find("div", class_ = "downloads")
            link = article.find('a')
            img_url = link['href']
            
            # Append the title and img_url to the list
            dictionary = {"title" : title, "img_url" : img_url}
            hemisphere_image_urls.append(dictionary)
            
        except:
            print("Error")

    return hemisphere_image_urls

    # Close the browser when done scraping
    browser.quit()

def scrape():
    # Call other functions
    news_dict = marsNews()
    image_dict ={"Featured Image" : marsImages()}
    facts_dict = {"Mars Facts" : marsFacts()}
    hemisphere_dict = marsHemispheres()

    # Convert all scraped data to a dictionary
    final_dict = {json.dumps(news_dict), json.dumps(image_dict), json.dumps(facts_dict), json.dumps(hemisphere_dict)}

    # Return the final_dict
    return final_dict

# Store the URL of the websites we will be scraping
news_url = "https://mars.nasa.gov/news/"
image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
facts_url = "https://space-facts.com/mars/"
hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"


final_dict = scrape()
print(final_dict)