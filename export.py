import os
import csv
import pickle
import argparse

# Arguments (argparse) options
parser = argparse.ArgumentParser(description='')
parser.add_argument('-o', '--output', type=str, required=False, default="data", help='Specify the output file filename (without extension)')
parser.add_argument('-i', '--input', type=str, required=False, default="data", help='Specify the input file (with extension)')      # not implemented
parser.add_argument('-t', '--type', type=str, required=False, default="csv", help='Specify the output type (csv...)')               # not implemented
args = parser.parse_args()

# Prepare CSV file
with open(f'{args.output}.csv', mode="w", newline='') as csv_file:
    fieldnames = ["id", "title", "price", "city", "post_date", "negotiable", "exchangeable", "description", "url"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

# Write to file
with open(f'output.pickle', "rb") as in_file: 
    MEGAad = pickle.load(in_file)

    for i in range(MEGAad["numberOfAds"]):
        # Save data to CSV
        with open(f'{args.output}.csv', mode="a", newline='') as csv_file:
            fieldnames = ["id", "title", "price", "city", "post_date", "negotiable", "exchangeable", "description", "url"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            try: writer.writerow({"id": i,"title": MEGAad[i]["title"], "price": MEGAad[i]["price"], "city": MEGAad[i]["city"], "post_date": MEGAad[i]["post_date"], "negotiable": MEGAad[i]["negotiable"], "exchangeable": MEGAad[i]["exchangeable"], "url": MEGAad[i]["url"]})
            except: pass
