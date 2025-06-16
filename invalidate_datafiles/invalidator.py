import os

#cmd = "crab-dev setfilestatus --status INVALID --file {}"
cmd = crab-dev setfilestatus --status INVALID --dataset {}

with open("files.txt") as f:
    files = [line.strip() for line in f.readlines()]


for file in files:
    #if '224201' in file:
    #    os.system(cmd.format(file))
    os.system(cmd.format(file))
