#!/bin/bash

PREFIX=""
INFIX=""



#SUFFIX="2022"; PREFIX="scenario"; INFIX="GENall_"
#SUFFIX="AODSIM_2022"
#SUFFIX="MINIAODSIM_2022"
#SUFFIX="MINIAODSIM_2022_postEE"

#SUFFIX="2023"; PREFIX="scenario"; INFIX="GENall_"
#SUFFIX="GENSIM_2023"
#SUFFIX="GENSIM_2023_postBPix"
#SUFFIX="DIGIRAW_2023"
#SUFFIX="DIGIRAW_2023_postBPix"
#SUFFIX="AODSIM_2023"
#SUFFIX="AODSIM_2023_postBPix"

#SUFFIX="2023-ext"; PREFIX="scenario"; INFIX="GENall_"
#SUFFIX="2023_postBPix-ext"; PREFIX="scenario"; INFIX="GENall_"
#SUFFIX="GENSIM_2023-v2_ext"
SUFFIX="GENSIM_2023_postBPix-v2_ext"
#SUFFIX="DIGIRAW_2023-ext"
#SUFFIX="DIGIRAW_2023_postBPix-ext"
#SUFFIX="AODSIM_2023-ext"
#SUFFIX="AODSIM_2023_postBPix-ext"

if [ -z "$1" ]
  then
    echo "No argument supplied"
else
    SUFFIX="$1"
fi


#dasgoclient --query="dataset=/*/tafoyava*_${SUFFIX}-*/* instance=prod/phys03" > output/datasets_${SUFFIX}.txt
dasgoclient --query="dataset=/*/tafoyava*${PREFIX}*_${SUFFIX}-*/* instance=prod/phys03" > output/datasets_${INFIX}${SUFFIX}.txt

# Retrieve details of each of the samples
rm -f output/results_${INFIX}${SUFFIX}.txt
while read p; do
    echo "$p"
    echo "$p" >> output/results_${INFIX}${SUFFIX}.txt
    echo "$( dasgoclient --query="summary dataset=$p instance=prod/phys03" )" >> output/results_${INFIX}${SUFFIX}.txt
    sleep 2
done <output/datasets_${INFIX}${SUFFIX}.txt
