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
output_file_dict_complete_duplicated = input_file+"_dictionary_complete_duplicated"

print(f"Processing {input_file}")

list_exceptions = list()
list_exceptions.append('scenarioB1_mpi_5_mA_2p40_ctau_0p1/tafoyava-DIGIRAW_2023-ext-') # error 8028: Input file root://cmsxrootd.fnal.gov//store/user/tafoyava/samples/GENSIM/scenarioB1_mpi_5_mA_2p40_ctau_0p1/GENSIM_2023-v2_ext/250403_182243/0000/output_998.root could not be opened.
list_exceptions.append('scenarioB1_mpi_4_mA_0p80_ctau_10/tafoyava-DIGIRAW_2023-ext-') #  error 8028: Input file root://cmsxrootd.fnal.gov//store/user/tafoyava/samples/GENSIM/scenarioB1_mpi_4_mA_0p80_ctau_10/GENSIM_2023-v2_ext/250403_171735/0000/output_621.root could not be opened.
list_exceptions.append('scenarioA_mpi_5_mA_0p50_ctau_0p1/tafoyava-DIGIRAW_2023_postBPix-ext-') # error -1: The framework job report could be loaded, but no error message was found there.
#list_exceptions.append('') # 

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

        # Labelling which datasets are processed under some sort of exception (e.g. failing to read an input root file)
        label = ''
#        for exception in list_exceptions:
#            if exception in path_line:
#                label = ',EXCEPTION_DATASET'

        # Write to the output file in the desired format
        outfile.write(f'"{identifier}": "{path_line}","nlumis":{nlumis},"nfiles":{nfiles}{label}\n')

print(f"	Summarised sample information written to {output_file}")



import re

def clean_file(output_file, output_file_dict):
    with open(output_file, 'r') as infile, open(output_file_dict, 'w') as outfile:
        for line in infile:
            cleaned_line = re.sub(r',"nfiles":\d+', '', line)  # Remove ,"nfiles":1000
            outfile.write("     " + cleaned_line)

### Check file completeness based on nfiles (fails if there are duplicate files)
def clean_file_OnlyFinishedSamples_nfiles(output_file, output_file_dict_complete):
    with open(output_file, 'r') as infile, open(output_file_dict_complete, 'w') as outfile:
        for line in infile:
            if '"nfiles":1000' in line and not ("scenarioB2" in line or "scenarioC" in line): # only completed scenarioA and scenarioB1 samples
                cleaned_line_1 = re.sub(r',"nfiles":\d+', '', line)  # Remove ,"nfiles":
                cleaned_line_2 = re.sub(r'"nlumis":\d+', '', cleaned_line_1)  # Remove ,"nlumis":
                outfile.write("     " + cleaned_line_2)

def clean_file_IncompleteSamples_nfiles(output_file, output_file_dict_incomplete):
    with open(output_file, 'r') as infile, open(output_file_dict_incomplete, 'w') as outfile:
        for line in infile:
            if '"nfiles":1000' not in line and not ("scenarioB2" in line or "scenarioC" in line): # only incomplete scenarioA and scenarioB1 samples are listed
                cleaned_line_1 = re.sub(r',"nfiles":\d+', '', line)  # Remove ,"nfiles":
                cleaned_line_2 = re.sub(r'"nlumis":\d+', '', cleaned_line_1)  # Remove ,"nlumis":
                outfile.write("     " + cleaned_line_2)


# Get the number of lumis from a give dataset's line, return as an integer
def get_nlumis_val(line):
    lumis_val=""
    parts = line.split('"nlumis":')
    if len(parts) > 1:
        lumis_str = parts[1].split(',')[0]  # Get the value before the next comma
        lumis_val = int(lumis_str)
        return lumis_val
    else:
        print("nlumis not found")

# Get the number of files from a give dataset's line, return as an integer
def get_nfiles_val(line):
    files_val=""
    parts = line.split('"nfiles":')
    if len(parts) > 1:
        files_str = parts[1].split(',')[0]  # Get the value before the next comma
        files_val = int(files_str)
        return files_val
    else:
        print("nfiles not found")

nlumis_val_reference=9000

### Check file completeness based on nlumis (robust to duplicate files)
def clean_file_OnlyFinishedSamples_nlumis(output_file, output_file_dict_complete):
    with open(output_file, 'r') as infile, open(output_file_dict_complete, 'w') as outfile:
        for line in infile:
            if not ("scenarioB2" in line or "scenarioC" in line): # only scenarioA and scenarioB1
               nlumis_val=get_nlumis_val(line)

#               if '"nlumis":10000' in line: # only completed samples are listed
               if nlumis_val >= nlumis_val_reference: # only samples completed above some value (e.g. 90%) are listed
                    cleaned_line_1 = re.sub(r',"nfiles":\d+', '', line)  # Remove ,"nfiles":
                    cleaned_line_2 = re.sub(r'"nlumis":\d+', '', cleaned_line_1)  # Remove ,"nlumis":
                    outfile.write("     " + cleaned_line_2)
#                elif '"nlumis":9990' in line:
#                    for exception in list_exceptions:
#                        if exception in line:
#                            cleaned_line_1 = re.sub(r',"nfiles":\d+', '', line)  # Remove ,"nfiles":
#                            cleaned_line_2 = re.sub(r'"nlumis":\d+', '', cleaned_line_1)  # Remove ,"nlumis":
#                            outfile.write("     " + cleaned_line_2)


def clean_file_IncompleteSamples_nlumis(output_file, output_file_dict_incomplete):
    with open(output_file, 'r') as infile, open(output_file_dict_incomplete, 'w') as outfile:
        for line in infile:
            if not ("scenarioB2" in line or "scenarioC" in line): # only scenarioA and scenarioB1
                nlumis_val=get_nlumis_val(line)

#                if '"nlumis":10000' not in line: # only incomplete samples are listed
                if nlumis_val < nlumis_val_reference: # only samples completed below some reference value (e.g. 90%) are listed
                    cleaned_line_1 = re.sub(r',"nfiles":\d+', '', line)  # Remove ,"nfiles":
                    cleaned_line_2 = re.sub(r'"nlumis":\d+', '', cleaned_line_1)  # Remove ,"nlumis":
                    outfile.write("     " + cleaned_line_2)

def clean_file_CompleteDuplicatedSamples(output_file, output_file_dict_complete_duplicated):
    with open(output_file, 'r') as infile, open(output_file_dict_complete_duplicated, 'w') as outfile:
        for line in infile:
            if not ("scenarioB2" in line or "scenarioC" in line): # only scenarioA and scenarioB1
                nlumis_val=get_nlumis_val(line)
                nfiles_val=get_nfiles_val(line)

#                if ('"nlumis":10000' in line and '"nfiles":1000' not in line): # only complete samples with duplicated files are listed
                if nlumis_val != 10*nfiles_val: # only samples with inconsistent nlumis and nfiles are listed
                    cleaned_line_1 = re.sub(r',"nfiles":\d+', '', line)  # Remove ,"nfiles":
                    cleaned_line_2 = re.sub(r'"nlumis":\d+', '', cleaned_line_1)  # Remove ,"nlumis":
                    outfile.write(line)
#                    outfile.write(cleaned_line + '\n')
#                    outfile.write("     " + cleaned_line_2)



# Usage
#clean_file(output_file, output_file_dict)

clean_file_OnlyFinishedSamples_nlumis(output_file, output_file_dict_complete)
print(f"	Dictionary of completed samples written to {output_file_dict_complete}")

clean_file_IncompleteSamples_nlumis(output_file, output_file_dict_incomplete)
print(f"	Dictionary of incomplete samples written to {output_file_dict_incomplete}")

clean_file_CompleteDuplicatedSamples(output_file, output_file_dict_complete_duplicated)
print(f"	Dictionary of duplicated samples written to {output_file_dict_complete_duplicated}")
