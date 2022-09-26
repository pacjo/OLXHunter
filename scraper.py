import pickle
import argparse
import requests
import requests_cache
import unidecode
from bs4 import BeautifulSoup

# Arguments (argparse) options
parser = argparse.ArgumentParser(description='')
parser.add_argument('url', type=str, help='url used for scrapint (without any filters')
parser.add_argument('-o', '--output', type=str, required=False, default="data", help='Specify the output file filename')
parser.add_argument('-v', '--verbose', action='store_true', help="Print command output (for testing)")

args = parser.parse_args()

main_url = "https://www.olx.pl"
ad_class = "css-19ucd76"
page_numbers_class = "pagination-item"
title_class = "css-v3vynn-Text"
price_class = "css-wpfvmn-Text"
ad_info_class = "css-p6wsjo-Text"
ad_url_class = "css-1bbgabe"
search_url = args.url        # e.g. https://www.olx.pl/d/elektronika/telefony/smartfony-telefony-komorkowe/q-note-10-pro
output_file = f"{args.output}.csv"

# Enable caching
requests_cache.install_cache('cache')

# Get 1st page
page = requests.get(search_url)
soup = BeautifulSoup(page.content, 'html.parser')

# Calculate number of pages
pages = soup.find_all(class_=page_numbers_class)
number_of_pages = pages[len(pages) - 1]['aria-label'][5:10]

# Scrape ads
ads = soup.find_all(class_=ad_class)

# Prepare output
MEGAad = {}

ads_count = 0
for page_number in range(int(number_of_pages)):
    page = requests.get(f"{search_url}/?page={page_number + 1}")
    soup = BeautifulSoup(page.content, 'html.parser')

    for n in range(len(ads)):
        try:
            ad = {
                "title": unidecode.unidecode(ads[n].find(class_=title_class).text),
                "url": main_url + ads[n].find(class_=ad_url_class)["href"],
                "price": (ads[n].find(class_=price_class).text),
                "city": unidecode.unidecode(ads[n].find(class_=ad_info_class).text[0:ads[n].find(class_=ad_info_class).text.find('-') - 1]),
                "post_date": unidecode.unidecode(ads[n].find(class_=ad_info_class).text[ads[n].find(class_=ad_info_class).text.find('-') + 2:len(ads[n].find(class_=ad_info_class).text)]),
                "negotiable": False,    # temp, changed later
                "exchangeable": False   # temp, changed later
            }
            ad["negotiable"] = True if ad["price"].find("do negocjacji") > -1 else False
            ad["exchangeable"] = True if ad["price"].find("Zamienię") > -1 else False
            ad["price"] = ad["price"][0:ad["price"].find("do negocjacji")] if ad["negotiable"] == True else ad["price"]
            ad["price"] = 0 if ad["exchangeable"] == True else ad["price"]
            ad["price"] = int(ad["price"][0:ad["price"][0:ad["price"].find("zł") - 1].find(',')].replace(' ', '')) if(ad["price"].find(',') > -1) else int(ad["price"][0:ad["price"].find("zł") - 1].replace(' ', ''))

            if(args.verbose): 
                print(f"\n\n{ads_count}: ======================================================================== - page: {page_number}, ad: {n}")
                print(ad)

            MEGAad[ads_count] = ad

            ads_count += 1

        except AttributeError:
            pass    # do nothing (good enough solution)

MEGAad["numberOfAds"] = ads_count

with open(f'output.pickle', "wb") as out_file: 
    pickle.dump(MEGAad, out_file)