#!/bin/bash

### Examples of the content of each variable
# HERE="/home/hep/jtafoyav/production_2023/tools/get_file_report/"
# WHERE="/home/hep/jtafoyav/production_2023/CMSSW_13_0_20/src/2023_GENSIM-v2_ext/"
# LIST_INCOMPLETE_FILES="/home/hep/jtafoyav/production_2023/tools/read_from_das/output/results_GENSIM_2023-v2_ext.txt_dictionary_incomplete"
# DATASET="scenarioA_mpi_10_mA_3p33_ctau_10"


HERE=$(pwd)
WHERE=$1
LIST_INCOMPLETE_FILES=$2
echo "Accting on samples: ${WHERE}"
echo " "
echo "Missing files read from $LIST_INCOMPLETE_FILES"
echo " "

DATA_LIST=${HERE}/dataset_list.txt

LIST_TO_RESUBMIT=${WHERE}/list_to_resubmit.txt
rm -f ${LIST_TO_RESUBMIT}

while read p; do
  DATASET=$p
  echo ${DATASET}
  if grep "${DATASET}/" ${LIST_INCOMPLETE_FILES} > /dev/null
  then
    echo "	Dataset incomplete. Getting report"
    echo ${DATASET} >> ${LIST_TO_RESUBMIT}
    crab report -d ${WHERE}/${DATASET}/crab_${DATASET}/ --output=${WHERE}/${DATASET}/crab_${DATASET}/results/
    #crab report -d ${WHERE}/${DATASET}/crab_${DATASET}/ --output=${WHERE}/crab_report/report_${DATASET}
    #crab report -d ${WHERE}/${DATASET}/crab_${DATASET}/
  fi
done <${DATA_LIST}

echo " "
echo "List of files to resubmit in ${LIST_TO_RESUBMIT}"

