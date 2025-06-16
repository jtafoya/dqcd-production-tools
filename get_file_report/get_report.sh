#!/bin/bash

WHERE=$1
echo ${WHERE}

DATA_LIST=dataset_list.txt

while read p; do
  DATASET=$p
  echo ${DATASET}
  crab report -d ${WHERE}/${DATASET}/crab_${DATASET}/ --output=${WHERE}/crab_report/report_${DATASET}
  #crab report -d ${WHERE}/${DATASET}/crab_${DATASET}/
done <${DATA_LIST}
#DATASET=scenarioA_mpi_10_mA_3p33_ctau_10

