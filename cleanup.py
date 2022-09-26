import os
import pickle
import argparse
import pprint

# Arguments (argparse) options
parser = argparse.ArgumentParser(description='')
parser.add_argument('-o', '--output', type=str, required=False, default="data", help='Specify the output file filename')
parser.add_argument('-v', '--verbose', action='store_true', help="Print command output (for testing)")
args = parser.parse_args()

# Remove duplicates
print("Removing duplicates")
with open(f'output.pickle', "r+b") as in_file: 
    MEGAad = pickle.load(in_file)
    pp = pprint.PrettyPrinter(indent=2)                      # black magic

    MEGAadFiltered = {}
    filtered_counter = 0
    for key, value in MEGAad.items():                        # https://tutorial.eyehunts.com/python/python-remove-duplicates-from-dictionary-example-code/
        if (value not in MEGAadFiltered.values()):
            MEGAadFiltered[key] = value
            filtered_counter += 1
    MEGAadFiltered["numberOfAds"] = filtered_counter         # update ad counter

# Print result
if(args.verbose):
    for i in range(MEGAadFiltered["numberOfAds"]):
        print(f'\n\n{i}: ========================================================================')
        try: print(MEGAadFiltered[i])
        except: pass

# Save result
with open(f'output.pickle', "wb") as out_file: 
    pickle.dump(MEGAadFiltered, out_file)