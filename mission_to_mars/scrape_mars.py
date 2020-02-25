def scrape():
    import pandas as pd
    import time
    import json
    import requests
    from splinter import Browser
    from bs4 import BeautifulSoup as bs
    
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    
#keys and dictionary setup
    mars_dict = []
    mars_values = []
    mars_dict_keys = ['News', 'Featured Image', 'Weather', 'Table', 'Hemisphere Images']
    
#mars news
    news_keys = ['News Title', 'News Caption']
    news_values = []
    news = []
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    news_title = soup.find('div', class_='image_and_description_container').find('h3').text
    news_title.strip

    news_p = soup.find('div', class_='article_teaser_body').text
    news_p.strip

    news_values.append(news_title)
    news_values.append(news_p)
    news.append(dict(zip(news_keys, news_values)))
    
#mars main image
    main_img = []
    main_img_keys = ["Main Image"]
    main_img_values = []
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    image = soup.find_all('a', class_='fancybox')[0]["data-fancybox-href"]
    site_root = "https://www.jpl.nasa.gov"
    featured_image_url = site_root + image
    main_img_values.append(featured_image_url)
    main_img.append(dict(zip(main_img_keys, main_img_values)))
    
#mars weather
    weather_keys = ['Current Weather']
    weather_values = []
    current_weather = []
    
    url = 'https://twitter.com/MarsWxReport'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')

    mars_weather = soup.find('p', class_="TweetTextSize").text
    weather_values.append(mars_weather)
    current_weather.append(dict(zip(weather_keys, weather_values)))
    
#mars table
    mars_table_keys = ['Table HTML']
    table_html = []
    table_value = []
    
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]
    html_table = df.to_html()
    table_value.append(html_table)
    table_html.append(dict(zip(mars_table_keys, table_value)))
    
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
    mars_values.append(news)
    mars_values.append(main_img)
    mars_values.append(current_weather)
    mars_values.append(table_html)
    mars_values.append(hemisphere_image_urls)
    mars_dict.append(dict(zip(mars_dict_keys, mars_values)))
    print(mars_dict)