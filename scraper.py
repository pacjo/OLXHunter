import csv
import requests
from bs4 import BeautifulSoup

main_url = "https://www.olx.pl"
ad_class = "css-19ucd76"
page_numbers_class = "pagination-item"
title_class = "css-v3vynn-Text"
price_class = "css-wpfvmn-Text"
ad_url_class = "css-1bbgabe"
search_url = "https://www.olx.pl/d/elektronika/telefony/smartfony-telefony-komorkowe/q-note-10-pro"

# Get 1st page
page = requests.get(search_url)
soup = BeautifulSoup(page.content, 'html.parser')

# Calculate number of pages
pages = soup.find_all(class_=page_numbers_class)
number_of_pages = pages[len(pages) - 1]['aria-label'][5:10]

# TODO: do for all pages
# Scrape ads
ads = soup.find_all(class_=ad_class)

for n in range(len(ads)):
    try:
        print(f'{n}: =========================================================================')

        ad_title = ads[n].find(class_=title_class).text
        ad_url = main_url + ads[n].find(class_=ad_url_class)["href"]  # somewhat of a url ?     -- to fix

        ad_price = ads[n].find(class_=price_class).text
        negotiable = True if ad_price.find("do negocjacji") > -1 else False
        exchange = True if ad_price.find("Zamienię") > -1 else False
        ad_price = ad_price[0:ad_price.find("do negocjacji")] if ad_price.find("do negocjacji") > -1 else ad_price

        print(ad_title)
        print(f"{ad_price}   negocjacje: {negotiable}   zamiana: {exchange}")
        print(ad_url)
    except AttributeError:
        # print("THERE WAS AN AD!!!")
        pass    # do nothing (good enough solution)

# Save data to file - also TODO