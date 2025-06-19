This repository is used to get back the report of the corresponding crab jobs. The report contains a list specifying what's the initial input of the job, and how many of those have been processed.

Get the report of incomplete files with e.g.:
```
cd /home/hep/jtafoyav/production_2023/tools/get_file_report/
python3 get_report.sh /home/hep/jtafoyav/production_2023/CMSSW_13_0_20/src/2023_GENSIM-v2_ext/ /home/hep/jtafoyav/production_2023/tools/read_from_das/output/results_GENSIM_2023-v2_ext.txt_dictionary_incomplete
```
