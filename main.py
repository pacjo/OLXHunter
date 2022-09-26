import os
import pickle
import argparse
import pprint
import re

# Arguments (argparse) options
parser = argparse.ArgumentParser(description='')
parser.add_argument('-o', '--output', type=str, required=False, default="data", help='Specify the output file filename')
parser.add_argument('url', type=str, help='url used for scrapint (without any filters')
parser.add_argument('--min', type=int, default=0, help="Minimal price of an item")
parser.add_argument('--max', type=int, default=10000000000, help="Maximal price of an item")
parser.add_argument('-r', '--regex', type=str, default="\"(xiaomi|redmi)? ?note ?(9|10|11) ?pro\"gmi", help="Regex used for validation of ad titles")
parser.add_argument('-v', '--verbose', action='store_true', help="Print command output (for testing)")
args = parser.parse_args()

# Run scraper
print("Scraping URL")
os.system(f"python scraper.py {args.url} -o {args.output} --verbose") if(args.verbose) else os.system(f"python scraper.py {args.url} -o {args.output}")

# Clean up the results
print("Cleaning results")
os.system(f"python cleanup.py -o {args.output} --verbose") if(args.verbose) else os.system(f"python cleanup.py -o {args.output}")
