import os
import json
import argparse
import re
import shutil
import time

# Arguments (argparse) options
parser = argparse.ArgumentParser(description='')
parser.add_argument('-o', '--output', type=str, required=False, default="data", help='Specify the output file filename')
parser.add_argument('-df', '--disable_fetch', action='store_true', help='Disable fetching new data')
parser.add_argument('-d', '--debug', action='store_true', help='Shows debug messages')
args = parser.parse_args()

# Run monitor OLX for changes
while True:
    if(args.disable_fetch != True):
        shutil.copy(f"{args.output}.json", f"last_{args.output}.json")
        os.system(f"python scraper.py -o {args.output}")
    file = open(f"{args.output}.json", 'r')
    current = json.load(file)
    file.close()
    file = open(f"last_{args.output}.json", 'r')
    last = json.load(file)
    file.close()

    for i in range(min(last["num_of_observed_ads"], current["num_of_observed_ads"])):
        if (int(current[str(i)]["number_of_ads"]) > int(last[str(i)]["number_of_ads"])):
            print("new listing found (" + current[str(i)]["number_of_ads"] + "): " + current[str(i)]["url"])

    time.sleep(30)
