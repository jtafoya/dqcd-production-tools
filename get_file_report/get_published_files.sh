#!/bin/bash

PREFIX=""
INFIX=""

#SUFFIX="2023-ext"; PREFIX="scenario"; INFIX="GENall_"
#SUFFIX="2023_postBPix-ext"; PREFIX="scenario"; INFIX="GENall_"
#SUFFIX="GENSIM_2023-v2_ext"
SUFFIX="GENSIM_2023_postBPix-v2_ext"
#SUFFIX="DIGIRAW_2023-ext"
#SUFFIX="DIGIRAW_2023_postBPix-ext"
#SUFFIX="AODSIM_2023-ext"
#SUFFIX="AODSIM_2023_postBPix-ext"

dasgoclient --query="dataset=/*/tafoyava*${PREFIX}*_${SUFFIX}-*/* instance=prod/phys03" > output/${SUFFIX}/datasets_${INFIX}${SUFFIX}.txt
