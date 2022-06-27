import os
import csv
import argparse
import re

# Arguments (argparse) options
parser = argparse.ArgumentParser(description='')
parser.add_argument('-o', '--output', type=str, required=False, default="data", help='Specify the output file filename')
parser.add_argument('url', type=str, help='url used for scrapint (without any filters')
parser.add_argument('--min', type=int, default=0, help="Minimal price of an item")
parser.add_argument('--max', type=int, default=10000000000, help="Maximal price of an item")
parser.add_argument('-r', '--regex', type=str, default="\"(xiaomi|redmi)? ?note ?(9|10|11) ?pro\"gmi", help="Regex used for validation of ad titles")
args = parser.parse_args()

# Run scraper
os.system(f"python scraper.py {args.url} -o {args.output}")

# Process the CSV
with open(f"{args.output}.csv", mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for ad in csv_reader:
        if(type(re.search(args.regex, ad["title"])) != None):
            print(ad["title"])
        