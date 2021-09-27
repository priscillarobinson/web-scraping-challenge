# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Run all scraping functions and store in dictionary
    data = {}

# Mars News
    url_news = 'https://redplanetscience.com/'
    browser.visit(url_news)

    #html object
    html_news = browser.html
    soup = BeautifulSoup(html_news, 'html.parser')

    # Collect latest news title and paragraph text
    title = soup.find_all('div',class_='content_title')
    paragraph = soup.find_all('div',class_='article_teaser_body')

    news_title = title[0].text
    paragraph_sum = paragraph[0].text

    print(news_title)
    print(paragraph_sum)

    data["news_title"] = news_title
    data["paragraph_sum"] = paragraph_sum
# Featured Image


    # visit URL for featured space image site. 
    # Use splinter to navigate the site and find the image url for the current Featured Mars Image 
    # assign the url string to a variable called featured_image_url
    url_image = 'https://spaceimages-mars.com/'
    browser.visit(url_image)

    html_image = browser.html
    img_soup = BeautifulSoup(html_image, 'html.parser')
    
    # retrieve element that contains image information
    featured_image = img_soup.find('div',class_='floating_text_area')
    # image_soup

    featured_image = img_soup.find('a',class_='showimg fancybox-thumbs').get("href")
    # image    
    featured_image = url_image + featured_image
    # image_url

    data["featured_image"] = featured_image

# Mars Facts

    # use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc
    # use Pandas to convert the data to a HTML table string
    mars_table = pd.read_html('https://galaxyfacts-mars.com/')
    

    mars_df = mars_table[1]
    
    mars_df.columns = ['description', 'value']
    #df.set_index('description', inplace=True)
    

    mars_facts = mars_df.to_html(index=False)
    
    data["mars_table"] = mars_facts

    # ### Mars Hemispheres


    # Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name.
    # Use a Python dictionary to store the data using the keys img_url and title.
    # Append the dictionary to store the data using the keys img_url and title
    # Append the dictionary with the image url string and hemisphere title to a list
    url_hemisphere = 'https://marshemispheres.com/'
    browser.visit(url_hemisphere)


    hemisphere_image_urls = []

    for i in range(4):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[i].click()
    #     time.sleep(1)
        html_hemisphere = browser.html
        hemi_soup = BeautifulSoup(html_hemisphere, "html.parser")
        hemisphere['img_url'] = url_hemisphere + hemi_soup.find("a", text="Sample").get("href")
        hemisphere['title'] = hemi_soup.find("h2", class_="title").get_text()
        hemisphere_image_urls.append(hemisphere)
        browser.back()
        
    # hemisphere_image_urls
    data["hemispheres"] = hemisphere_image_urls

    browser.quit()

    return data 


