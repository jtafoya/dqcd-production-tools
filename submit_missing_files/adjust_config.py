import sys
import re

input_file = ""

if len(sys.argv) == 2 :
        input_file = sys.argv[1]

print(f"ADJUSTING FILE: {input_file}")


# Read the file and check if the line already exists. If it doesn't, the line gets appended
def append_line_if_missing(input_file, new_line):

    with open(input_file, 'r') as file:
        lines = file.read().splitlines()  # Avoids '\n' issues when comparing

    if new_line not in lines:
        with open(input_file, 'a') as file:
            #file.write('\n')
            file.write(new_line + '\n')
        print(f"Line added: {new_line}")
    else:
        print("Line already exists. No changes made.")


# Fixing/changing output path
print(" ")
print(f"Changing crab job output path")
def correct_path(input_file):
    with open(input_file, 'r') as f:
        content = f.read()

    if "-ext/_resubmit/" in content:
        print("No changes made: '-ext/_resubmit/' already present.")
        return

    updated_content = content.replace("-ext/", "-ext/_resubmit/")

    with open(input_file, 'w') as f:
        f.write(updated_content)


import json

def append_inputFiles(input_file, filesToProcess, processedFiles):
    print(f"Reading file: {input_file}")

    # Load all input files
    with open(filesToProcess) as f:
        all_files = json.load(f)

    # Load processed file numbers
    with open(processedFiles) as f:
        processed_files = json.load(f)

    # Convert processed file numbers to ints for comparison (if needed)
    processed_ids = set(int(k) for k in processed_files.keys())

    # Filter: keep only files whose job ID is NOT in processed_ids
    unprocessed_files = [
        path[0] for jid, path in all_files.items()
        if int(jid) not in processed_ids
    ]

    # Check whether userInputFiles is already there
    with open(input_file, 'r') as f:
        content = f.read()

    if "config.Data.userInputFiles" in content:
        print("No changes made: 'config.Data.userInputFiles' already present.")
        return


    # Writing list of missing inputs
    with open(input_file, 'a') as file:
        file.write("config.Data.userInputFiles = [")
        for line in unprocessed_files:
            file.write(f'    "{line}",')
        file.write("]")

    print(f"Added custom list of inputs")



# Appending specific lines
append_line_if_missing(input_file, '\n')
append_line_if_missing(input_file, 'config.Site.blacklist = [\'T2_US_MIT\']')
append_line_if_missing(input_file, 'config.Site.whitelist = [\'T2_US_UCSD\',\'T2_US_Wisconsin\',\'T2_US_Florida\']')
append_line_if_missing(input_file, '\n')

# Adding "_resubmit/" to config file path
correct_path(input_file)

# Adding list of missing (i.e. unprocessed) files
#crab_submit_scenarioA_mpi_1_mA_0p25_ctau_100.py
#dataset="scenarioA_mpi_1_mA_0p25_ctau_100"
step='CMSSW_13_0_14/src/2023_DIGIRAW-ext/'
match = re.search(r'crab_submit_(.*)\.py$', input_file)
if match:
    dataset = match.group(1)
path='/home/hep/jtafoyav/production_2023/'+step+dataset+'/crab_'+dataset+'/results/'
print(f"{path}")

filesToProcess=path+'filesToProcess.json'
processedFiles=path+'processedFiles.json'
append_inputFiles(input_file, filesToProcess, processedFiles)
