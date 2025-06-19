#!/bin/bash

echo " "


PREFIX=""
INFIX=""

#SUFFIX="2023-ext"; PREFIX="scenario"; INFIX="GENall_"
#SUFFIX="2023_postBPix-ext"; PREFIX="scenario"; INFIX="GENall_"
SUFFIX="GENSIM_2023-v2_ext"
#SUFFIX="GENSIM_2023_postBPix-v2_ext"
#SUFFIX="DIGIRAW_2023-ext"
#SUFFIX="DIGIRAW_2023_postBPix-ext"
#SUFFIX="AODSIM_2023-ext"
#SUFFIX="AODSIM_2023_postBPix-ext"

DATASETS_OUTFILE="output/${SUFFIX}/datasets_${INFIX}${SUFFIX}.txt"
dasgoclient --query="dataset=/*/tafoyava*${PREFIX}*_${SUFFIX}-*/* instance=prod/phys03" > ${DATASETS_OUTFILE}
echo "-> List of datasets saved to ${DATASETS_OUTFILE}"
echo " "

DATASET_FULL="/scenarioA_mpi_2_mA_0p25_ctau_10/tafoyava-GENSIM_2023-v2_ext-193c693ae8e80199a98cd4c3b274ad5a/USER"
DATASET="scenarioA_mpi_2_mA_0p25_ctau_10"
OUTFILE="output/${SUFFIX}/file-list_${DATASET}.txt"

echo "Working on ${DATASET}"
dasgoclient -query="file dataset=${DATASET_FULL} instance=prod/phys03" > ${OUTFILE}
echo " List of files saved to ${OUTFILE}"
