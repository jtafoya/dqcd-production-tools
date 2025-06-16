import os
import time
import random
import string
import sys
import json
from copy import deepcopy as copy

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-f','--folder', dest='folder', default='/home/hep/jtafoyav/production_2023/CMSSW_13_0_14/src/2023_DIGIRAW-ext/')
parser.add_argument('-d','--dataset', action='store_true', default=False)
parser.add_argument('-r','--resubmit', action='store_true', default=False)
parser.add_argument('-e','--end', action='store_true', default=False)
parser.add_argument('-k','--kill', action='store_true', default=False)
parser.add_argument('-auto','--auto-resubmit', action='store_false', default=True)

dict_format = True
resub_wall_time = 2000

options = parser.parse_args()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def randomize(input_string):
    random_str = "".join(random.choice(string.ascii_letters) for _ in range(10))
    return "{}_{}".format(input_string, random_str)

print(f"   ")
print(f"ACTING ON {options.folder}")
print(f"   ")

# Retrieve a list of ALL relevant datasets
path_datasets_all="/home/hep/jtafoyav/production_2023/tools/status_smarter/datasets_scenarios.txt"
print(f"List of all datasets fetched from {path_datasets_all}:")
with open(path_datasets_all, 'r') as file_all:
    # Read all lines into a list
    names_all = [line.strip() for line in file_all]
print(f"{names_all}")

print("  ")

# Retrieve a list of all FINISHED datasets (see /home/hep/jtafoyav/production_2023/tools/read_from_das/)
path_datasets_finished="/home/hep/jtafoyav/production_2023/tools/read_from_das/output/results_DIGIRAW_2023-ext.txt_dictionary"
print(f"List of finished datasets fetched from {path_datasets_finished}:")
with open(path_datasets_finished, 'r') as file_finished:
    # Read all lines into a list
    list = [line.strip() for line in file_finished]
names_finished = [(n.split(":")[0]).replace('"', '') for n in list]
print(f"{names_finished}")


print("   ")


# Script will act ONLY on datasets that have not been finished yet. These are stored in the list "names"
names = [item for item in names_all if item not in names_finished]
number_names = len(names)
print(f"Checking {number_names} datasets:")
print(f"{names}")

cmnd = "%s/{name}/crab_{name}/" % options.folder
#cmnd = "crab status -d %s/{name}_2022/crab_{name}_2022/" % options.folder
maxlen = max([len(name) for name in names])

status_d = {}

def auto_resubmitter(lines):
    max_memory_val = 0
    mem_tag = "RSS="
    killed_job_tag = "wall clock limit"
    was_killed = False
    for line in lines:
        index = line.find(mem_tag)
        if index != -1:  # found!
            mem_val = int(line[index + len(mem_tag):].split(" ")[0])
            if mem_val > max_memory_val:
                max_memory_val = mem_val
        if line.find(killed_job_tag) != -1:
            was_killed = True
    return max_memory_val, was_killed

new_names = copy(names)
while True:
    names = copy(new_names)
    for name in names:
        #if "scenarioA" not in name:
        #if not any(scenario in name for scenario in ["scenarioB1","scenarioB2"]):
        #if "scenarioC" not in name:
        if not any(scenario in name for scenario in ["scenarioA","scenarioB1","scenarioB2","scenarioC"]):
            continue
        r = randomize("tmp")
        if not os.path.exists(cmnd.format(name=name)):
            continue
        if options.kill:
            os.system("crab kill -d {}".format(cmnd.format(name=name)))
            continue
        os.system("crab status -d {} > {}".format(cmnd.format(name=name), r))

        with open(r) as f:
            lines = f.readlines()
        os.system("rm %s" % r)

        if options.dataset:
            dataset = None
            for line in lines:
                if "Output dataset" in line:
                    line = line.strip().split("\t")
                    dataset = line[-1]
                    break
            if dataset:
                if not dict_format:
                    print(f"{name}: {dataset}")
                else:
                    print(f'"{name}": "{dataset}",')
            else:
                print("No dataset info for %s" % name)
            continue

        status = {
            "running": 0,
            "idle": 0,
            "finished": 0,
            "transferring": 0,
            "failed": 0,
            "killed": 0,
            "done": 0,
        }
        for line in lines:
            line = line.replace("\t", "  ")
            for key in status:
                if key + "  " in line:
                    status[key] = int(line.split("(")[-1].split("/")[0])

        if status["finished"] > 0 and status["done"] == status["finished"] and sum([st for st in status.values()]) == 2 * status["finished"]:
            print("%s%s finished.%s" % (bcolors.OKGREEN, name, bcolors.ENDC))
            new_names.remove(name)
            continue

        if options.end:
            continue

        run_status = "{:>3d}".format(status["running"])
        if status["running"] > 0:
            run_status = bcolors.OKBLUE + run_status + bcolors.ENDC

        fin_status = "{:>3d}".format(status["finished"])
        if status["finished"] > 0:
            fin_status = bcolors.OKGREEN + fin_status + bcolors.ENDC

        print("{name:<{size}s}: idle:{idle:>3d}, running:{run}, transferring:{transf:>3d}, finished:{fin} (transf:{done:>3d})".format(
            name=name, size=maxlen, idle=status["idle"], run=run_status, transf=status["transferring"], fin=fin_status, done=status["done"]
        ), end=""),
        if status["failed"] > 0 or status["killed"] > 0:
            print(", {}FAILED:{:>3d}{}".format(bcolors.FAIL, status["failed"] + status["killed"], bcolors.ENDC))
            print("Some job(s) failed. Try running {}crab status -d {} --verboseErrors{}".format(
                bcolors.BOLD, cmnd.format(name=name), bcolors.ENDC))
            if options.resubmit:
                os.system("crab resubmit -d {} --maxmemory=4500 --maxjobruntime=2000 --siteblacklist=T2_US_MIT --sitewhitelist=T2_US_UCSD,T2_US_Wisconsin,T2_US_Florida".format(cmnd.format(name=name)))

            if options.auto_resubmit:
                os.system("crab status -d {} --verboseErrors > {}".format(cmnd.format(name=name), r))
                with open(r) as f:
                    lines = f.readlines()
                os.system("rm %s" % r)
                max_memory_val, was_killed = auto_resubmitter(lines)
                if max_memory_val != 0 or was_killed:
                    cmd = "crab resubmit -d {} --siteblacklist=T2_US_MIT --sitewhitelist=T2_US_UCSD,T2_US_Wisconsin,T2_US_Florida".format(cmnd.format(name=name))
                    if max_memory_val != 0:
                        cmd += f" --maxmemory={max_memory_val + 250}"
                    if was_killed:
                        cmd += f" --maxjobruntime={resub_wall_time}"
                    print("--> Running " + cmd)
                    os.system(cmd)
        else:
            print()

        status_d[name] = status

    if any([options.dataset, options.resubmit, options.end, options.kill]):
        break

    outname = "_".join(options.folder.split("/"))
    if outname.endswith("_"):
        outname = outname[:-1]
    with open(outname + ".json", "w+") as f:
        json.dump(status_d, f, indent=4)

    if len(new_names) == 0:
        print("All jobs are finished.")
        break
    print("Waiting for 1 minute...")
    time.sleep(1 * 60)
    
    
