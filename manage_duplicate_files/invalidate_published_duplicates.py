import re
import os
import glob
import time
import subprocess
from collections import defaultdict

def clean_old_files(pattern="duplicates*.txt"):
    """Deletes all files matching the given pattern"""
    print(f"Removing all files in {pattern}")
    for file in glob.glob(pattern):
        os.remove(file)


def get_dataset_list(prefix, infix, suffix, output_file):
    try:
        cmd = ["dasgoclient", "-query", f"dataset=/*/tafoyava*{prefix}*_{suffix}-*/* instance=prod/phys03"]
        #result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        #file_list = result.stdout.strip().split('\n')
        #return file_list
        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        dataset_list = result.stdout.strip().split('\n')

        with open(output_file, "w") as f:
            for dataset in dataset_list:
                f.write(dataset + "\n")

        print(f"Found {len(dataset_list)} published datasets, saved to {output_file}")
        print(" ")
        return dataset_list

    except subprocess.CalledProcessError as e:
        print("Error running dasgoclient:", e.stderr)
        return []

def get_dataset_files(dataset_name, output_file):
    try:
        cmd = ["dasgoclient", "-query", f"file lumi status=VALID dataset={dataset_name} instance=prod/phys03"]
        #print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        file_list = result.stdout.strip().split('\n')

        # Save to file
        with open(output_file, "w") as f:
            for filename in file_list:
                f.write(filename + "\n")

        print(f"Found {len(file_list)} files published as VALID, saved to {output_file}")
        return file_list


    except subprocess.CalledProcessError as e:
        print("Error running dasgoclient:", e.stderr)
        return []


def extract_output_index(filename):
    """Extracts the number from output_*.root"""
    match = re.search(r'output_(\d+)\.root', filename)
    return int(match.group(1)) if match else None

def get_list_duplicated_files(dataset_file_list, output_file):
    # Map from index to list of full file paths
    index_map = defaultdict(list)

    with open(dataset_file_list, 'r') as f:
        for line in f:
            filepath = line.strip()
            idx = extract_output_index(filepath)
            if idx is not None:
                index_map[idx].append(filepath)

    # Filter: keep only indexes that appear more than once (duplicates)
    duplicates = []
    non_duplicate_count = 0

    for idx, files in index_map.items():
        if len(files) > 1:
            # Keep all duplicates except the first one
            duplicates.extend(files[1:])
        else:
            non_duplicate_count += 1

    if non_duplicate_count < 1000:
        print(f"	Incomplete dataset! Found only {non_duplicate_count} non-duplicated files")

    # Don't save anything if there are no duplicates
    if len(duplicates) == 0:
        return

    # Save to output file
    with open(output_file, 'w') as f:
        for dup in duplicates:
            f.write(dup + '\n')

    print(f"	Found {len(duplicates)} duplicate files. Saved to {output_file}")


def get_list_duplicate_lumi_files(input_file, output_file):
    seen_lumi_sets = {}
    duplicates = []

    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                file_path, lumis_str = line.split(' ', 1)
                lumis_str = lumis_str.strip()
                if lumis_str.startswith('[') and lumis_str.endswith(']'):
                    lumis_str = lumis_str[1:-1]
                lumis_list = [int(x.strip()) for x in lumis_str.split(',') if x.strip()]
                lumi_key = frozenset(lumis_list)

                if lumi_key in seen_lumi_sets:
                    duplicates.append(line)
                    #print(f"Duplicate lumi blocks found for:\n  {file_path}\n  duplicates {seen_lumi_sets[lumi_key]}\n")
                else:
                    seen_lumi_sets[lumi_key] = file_path

            except Exception as e:
                print(f"Skipping malformed line:\n{line}\nError: {e}")

    if len(duplicates) == 0:
        return
    else:
        with open(output_file, 'w') as f:
            for dup in duplicates:
                f.write(dup + '\n')
        print(f"	Saved {len(duplicates)} duplicate files to {output_file}")


def invalidate_duplicate_lumi_files(duplicates_file):

    with open(duplicates_file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        file_path = line.strip().split(' ', 1)[0]
        if not file_path.startswith('/store'):
            print(f"Skipping invalid path: {file_path}")
            continue

        cmd = [
            "crab-dev", "setfilestatus",
            "--files", file_path,
            "--status", "INVALID"
        ]

        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            print(f"Success: {result.stdout.strip()}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to set status for {file_path}: {e.stderr.strip()}")


def invalidate_duplicate_lumi_files_background(duplicates_file):
    max_parallel=50

    if not os.path.exists(duplicates_file):
        print(f"	File of duplicates not found: {duplicates_file}. Doing nothing.")
        return

    processes = []
    with open(duplicates_file, 'r') as f:
        for idx, line in enumerate(f, start=1):
            file_path = line.strip().split(' ', 1)[0]
            if not file_path.startswith('/store'):
                print(f"Skipping invalid path: {file_path}")
                continue

            cmd = [
                "crab-dev", "setfilestatus",
                "--files", file_path,
                "--status", "INVALID"
            ]

            # Launch in background
            print(f"[{idx}] Launching: {file_path}")
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            processes.append((file_path, proc))

            # Throttle if too many are running
            while len(processes) >= max_parallel:
                time.sleep(0.5)
                # Clean up finished processes
                processes = [(fp, p) for fp, p in processes if p.poll() is None]


    print("	Waiting for all background processes to finish...")
    # Wait for all to finish
    for file_path, proc in processes:
        stdout, stderr = proc.communicate()
        if proc.returncode == 0:
            print(f"	SUCCESS: {file_path}\n    {stdout.strip()}")
        else:
            print(f"	FAILED: {file_path}\n    {stderr.strip()}")

    print("	All `setfilestatus` commands have completed.")



prefix=""
infix=""

#suffix="2023-ext"; prefix="scenario"; infix="GENall_"
#suffix="2023_postBPix-ext"; prefix="scenario"; infix="GENall_"
#suffix="GENSIM_2023-v2_ext"
#suffix="GENSIM_2023_postBPix-v2_ext"
#suffix="DIGIRAW_2023-ext"
suffix="DIGIRAW_2023_postBPix-ext"
#suffix="AODSIM_2023-ext"
#suffix="AODSIM_2023_postBPix-ext"



## CLEAN OLD FILES

path_output_files="output/"+suffix+"/*txt"
clean_old_files(path_output_files)



# GET ENTIRE LIST OF DATASETS OFF OF DAS

print(" ")
dataset_list_outfile="output/"+suffix+"/datasets_"+infix+suffix+".txt"
dataset_list=get_dataset_list(prefix, infix, suffix, dataset_list_outfile)
#print(f"Found {len(dataset_list)} datasets")
#for f in dataset_list[:5]:
#    print(f)



## FOR EACH OF THE DATASETS, GET THE LIST OF PUBLISHED FILES AND GET A LIST OF FILES IN EACH OF THEM WITH DUPLICATED LUMI BLOCKS AND INVALIDATE THEM

#for dataset_path in dataset_list[:5]:
#for dataset_path in dataset_list[-5:]:
for dataset_path in dataset_list:
    dataset=dataset_path.split("/")[1]
    datafile_list_output="output/"+suffix+"/file-list_"+dataset+".txt"
    datafile_duplicated_list_output="output/"+suffix+"/duplicated-file-list_"+dataset+".txt"

    files = get_dataset_files(dataset_path, datafile_list_output)
    #print(f"Found {len(files)} files")
    #for f in files[:5]:
    #    print(f)

    #get_list_duplicated_files(datafile_list_output, datafile_duplicated_list_output)
    get_list_duplicate_lumi_files(datafile_list_output, datafile_duplicated_list_output)

    #invalidate_duplicate_lumi_files(datafile_duplicated_list_output)
    invalidate_duplicate_lumi_files_background(datafile_duplicated_list_output)
