import os
import subprocess

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

        print(f"Saved {len(dataset_list)} datasets to {output_file}")
        print(" ")
        return dataset_list

    except subprocess.CalledProcessError as e:
        print("Error running dasgoclient:", e.stderr)
        return []

def get_dataset_files(dataset_name, output_file):
    try:
        cmd = ["dasgoclient", "-query", f"file dataset={dataset_name} instance=prod/phys03"]
        #print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)

        file_list = result.stdout.strip().split('\n')

        # Save to file
        with open(output_file, "w") as f:
            for filename in file_list:
                f.write(filename + "\n")

        print(f"Saved {len(file_list)} files to {output_file}")
        return file_list


    except subprocess.CalledProcessError as e:
        print("Error running dasgoclient:", e.stderr)
        return []


prefix=""
infix=""

#suffix="2023-ext"; prefix="scenario"; infix="GENall_"
#suffix="2023_postBPix-ext"; prefix="scenario"; infix="GENall_"
#suffix="GENSIM_2023-v2_ext"
suffix="GENSIM_2023_postBPix-v2_ext"
#suffix="DIGIRAW_2023-ext"
#suffix="DIGIRAW_2023_postBPix-ext"
#suffix="AODSIM_2023-ext"
#suffix="AODSIM_2023_postBPix-ext"

print(" ")
dataset_list_outfile="output/"+suffix+"/datasets_"+infix+suffix+".txt"
dataset_list=get_dataset_list(prefix, infix, suffix, dataset_list_outfile)
#print(f"Found {len(dataset_list)} datasets")
#for f in dataset_list[:5]:
#    print(f)

#for dataset_path in dataset_list[:5]:
for dataset_path in dataset_list:
    dataset=dataset_path.split("/")[1]
    datafile_list_output="output/"+suffix+"/file-list_"+dataset+".txt"

    files = get_dataset_files(dataset_path, datafile_list_output)
    #print(f"Found {len(files)} files")
    #for f in files[:5]:
    #    print(f)
