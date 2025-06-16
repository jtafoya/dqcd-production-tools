import sys

input_file = ""

if len(sys.argv) == 2 :
	input_file = sys.argv[1]
else :
	print(f" ")
	print(f" ")
	print(f"WARNING! ")
	print(f" ")
	print(f"Must provide a single argument containing the name of the results.txt file")
	print(f" ")
	print(f" ")
	print(f"If results.txt doesn't exist, generate it by running e.g. ")
	print(f"	dasgoclient --query=\"dataset=/*/tafoyava*_GENSIM_2023_post*/* instance=prod/phys03\" > datasets.txt")
	print(f" ")
	print(f"and then")
	print(f"	rm results.txt")
	print(f"	while read p; do")
	print(f"    		echo \"$p\"")
	print(f"    		echo \"$p\" >> results.txt")
	print(f"    		echo \"$( dasgoclient --query=\"summary dataset=$p instance=prod/phys03\" )\" >> results.txt")
	print(f"    		sleep 2")
	print(f"	done <datasets.txt")
	print(f" ")
	print(f" ")
	exit()

output_file = input_file+"_formated"
output_file_dict_complete = input_file+"_dictionary"
output_file_dict_incomplete = input_file+"_dictionary_incomplete"

print(f"Processing {input_file}")

import json
# Open the input file for reading and the output file for writing
with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    lines = infile.readlines()

    # Process each pair of lines in the file
    for i in range(0, len(lines), 2):
        # Get the path line and the JSON data line
        path_line = lines[i].strip()
        json_data_line = lines[i + 1].strip()

        # Extract the unique identifier from the path line (removing initial slash)
        identifier = path_line.split('/')[1]

        # Parse the JSON data line and extract the "nfiles" value
#        json_data = eval(json_data_line)  # Use eval for simplified parsing, but for secure parsing, use `json.loads(json_data_line)`
        json_data = json.loads(json_data_line) # Using secure parsing
        nfiles = json_data[0]["nfiles"]
        nlumis = json_data[0]["nlumis"]

        # Write to the output file in the desired format
        outfile.write(f'"{identifier}": "{path_line}","nlumis":{nlumis},"nfiles":{nfiles}\n')

print(f"	Summarised sample information written to {output_file}")



import re

def clean_file(output_file, output_file_dict):
    with open(output_file, 'r') as infile, open(output_file_dict, 'w') as outfile:
        for line in infile:
            cleaned_line = re.sub(r',"nfiles":\d+', '', line)  # Remove ,"nfiles":1000
#            outfile.write(cleaned_line + '\n')
            outfile.write("     " + cleaned_line)

### Check file completeness based on nfiles (fails if there are duplicate files)

def clean_file_OnlyFinishedSamples_nfiles(output_file, output_file_dict_complete):
    with open(output_file, 'r') as infile, open(output_file_dict_complete, 'w') as outfile:
        for line in infile:
            if '"nfiles":1000' in line and not ("scenarioB2" in line or "scenarioC" in line): # only completed scenarioA and scenarioB1 samples
                cleaned_line_1 = re.sub(r',"nfiles":\d+', '', line)  # Remove ,"nfiles":
                cleaned_line_2 = re.sub(r'"nlumis":\d+', '', cleaned_line_1)  # Remove ,"nlumis":
#                outfile.write(cleaned_line + '\n')
                outfile.write("     " + cleaned_line_2)

def clean_file_IncompleteSamples_nfiles(output_file, output_file_dict_incomplete):
    with open(output_file, 'r') as infile, open(output_file_dict_incomplete, 'w') as outfile:
        for line in infile:
            if '"nfiles":1000' not in line and not ("scenarioB2" in line or "scenarioC" in line): # only incomplete scenarioA and scenarioB1 samples are listed
                cleaned_line_1 = re.sub(r',"nfiles":\d+', '', line)  # Remove ,"nfiles":
                cleaned_line_2 = re.sub(r'"nlumis":\d+', '', cleaned_line_1)  # Remove ,"nlumis":
#                outfile.write(cleaned_line + '\n')
                outfile.write("     " + cleaned_line_2)

### Check file completeness based on nlumis (robust to duplicate files)

def clean_file_OnlyFinishedSamples_nlumis(output_file, output_file_dict_complete):
    with open(output_file, 'r') as infile, open(output_file_dict_complete, 'w') as outfile:
        for line in infile:
            if '"nlumis":10000' in line and not ("scenarioB2" in line or "scenarioC" in line): # only completed scenarioA and scenarioB1 samples
                cleaned_line_1 = re.sub(r',"nfiles":\d+', '', line)  # Remove ,"nfiles":
                cleaned_line_2 = re.sub(r'"nlumis":\d+', '', cleaned_line_1)  # Remove ,"nlumis":
#                outfile.write(cleaned_line + '\n')
                outfile.write("     " + cleaned_line_2)

def clean_file_IncompleteSamples_nlumis(output_file, output_file_dict_incomplete):
    with open(output_file, 'r') as infile, open(output_file_dict_incomplete, 'w') as outfile:
        for line in infile:
            if '"nlumis":10000' not in line and not ("scenarioB2" in line or "scenarioC" in line): # only incomplete scenarioA and scenarioB1 samples are listed
                cleaned_line_1 = re.sub(r',"nfiles":\d+', '', line)  # Remove ,"nfiles":
                cleaned_line_2 = re.sub(r'"nlumis":\d+', '', cleaned_line_1)  # Remove ,"nlumis":
#                outfile.write(cleaned_line + '\n')
                outfile.write("     " + cleaned_line_2)



# Usage
#clean_file(output_file, output_file_dict)

clean_file_OnlyFinishedSamples_nlumis(output_file, output_file_dict_complete)
print(f"	Dictionary of completed samples written to {output_file_dict_complete}")

clean_file_IncompleteSamples_nlumis(output_file, output_file_dict_incomplete)
print(f"	Dictionary of incomplete samples written to {output_file_dict_incomplete}")
