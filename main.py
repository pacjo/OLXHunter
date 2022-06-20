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

# TODO: for all pages
# Scrape ads
ads = soup.find_all(class_=ad_class)
number_of_ads = len(ads)
# print(number_of_ads)

n = 0
ad_title = ads[n].find(class_=title_class).text
ad_price = ads[n].find(class_=price_class).text  # TODO: devide "do negocjacji" into another category
ad_url = main_url + ads[n].find(class_=ad_url_class)["href"]  # somewhat of a url ?     -- to fix
print(ad_title)
print(ad_price)
print(ad_url)

# Save data to file
