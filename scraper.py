import csv
import requests
import requests_cache
from bs4 import BeautifulSoup

main_url = "https://www.olx.pl"
ad_class = "css-19ucd76"
page_numbers_class = "pagination-item"
title_class = "css-v3vynn-Text"
price_class = "css-wpfvmn-Text"
ad_url_class = "css-1bbgabe"
search_url = "https://www.olx.pl/d/elektronika/telefony/smartfony-telefony-komorkowe/q-note-10-pro"
output_file = "data.csv"

# Enable caching
requests_cache.install_cache('cache')

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
        print(f'\n{n}: =========================================================================')

        ad = {
            "title": ads[n].find(class_=title_class).text,
            "url": main_url + ads[n].find(class_=ad_url_class)["href"],
            "price": ads[n].find(class_=price_class).text,
            "negotiable": False,    # temp, changed later
            "exchangeable": False   # temp, changed later
        }
        ad["negotiable"] = True if ad["price"].find("do negocjacji") > -1 else False
        ad["exchangeable"] = True if ad["price"].find("Zamienię") > -1 else False
        ad["price"] = ad["price"][0:ad["price"].find("do negocjacji")] if ad["price"].find("do negocjacji") > -1 else ad["price"]

        print(ad)
    except AttributeError:
        pass    # do nothing (good enough solution)

    # with open(output_file) as csv_file:
    #     csv_reader = csv.reader(csv_file, delimiter=',')


# Save data to file - also TODO