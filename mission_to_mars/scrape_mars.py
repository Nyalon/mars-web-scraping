def scrape():
    import pandas as pd
    import time
    import json
    import requests
    from splinter import Browser
    from bs4 import BeautifulSoup as bs
    
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    
#mars news
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find('div', class_='image_and_description_container').find('h3').text
    news_title.strip

    news_p = soup.find('div', class_='article_teaser_body').text
    news_p.strip
    
#mars main image
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    image = soup.find_all('a', class_='fancybox')[0]["data-fancybox-href"]
    site_root = "https://www.jpl.nasa.gov"
    featured_image_url = site_root + image
    
#mars weather  
    url = 'https://twitter.com/MarsWxReport'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')

    mars_weather = soup.find('p', class_="TweetTextSize").text
    
#mars table
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    html_table = df.to_html()
    
#hemispheres 
    itteration = ['Cerberus Hemisphere Enhanced', 'Schiaparelli Hemisphere Enhanced', 'Syrtis Major Hemisphere Enhanced', 'Valles Marineris Hemisphere Enhanced']
    keys = ['title', 'img_url']
    hemisphere_image_urls = []
    values = []

    for x in itteration:
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)

        time.sleep(4)

        browser.click_link_by_partial_text(x)
    
        html = browser.html
        soup = bs(html, 'html.parser')

        img = soup.find('img', class_='wide-image')['src']
        name = soup.find('h2', class_='title').text
        site_root = 'https://astrogeology.usgs.gov/'
        img_url = site_root + img

        values.append(name)
        values.append(img_url)
        hemisphere_image_urls.append(dict(zip(keys, values)))
        values = []
    
    mars_dict = {
        "news_title": news_title,
        "news_caption": news_p,
        "main_image": featured_image_url,
        "current_weather": mars_weather,
        "table_html": html_table,
        "hemisphere": hemisphere_image_urls
    }
    browser.quit()
    return mars_dict