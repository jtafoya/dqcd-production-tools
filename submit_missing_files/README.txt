New submissions should

### blacklist MIT:
config.Site.blacklist = 'T2_US_MIT'

Note that every one of the previously created submision files has a line
config.Site.storageSite = 'T2_US_UCSD'
at the end. The script add_blacklist.py adds the line if it doesn't exist


### whitelist UCSD, Wisconsin and Florida


### Submit ONLY the missing files to avoid duplicates
taskALumis = getLumiListInValidFiles(dataset=<TaskA-output-dataset-name>, dbsurl='phys03')
officalLumiMask = LumiList(filename='<some-kosher-name>.json')
newLumiMask = officialLumiMask - taskALumis
newLumiMask.writeJSON('my_lumi_mask.json')
config.Data.lumiMask = 'my_lumi_mask.json'
config.Data.outputDatasetTag = <TaskA-outputDatasetTag> 

See https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3FAQ#Recovery_task
See https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3FAQ#Dealing_with_a_growing_input_dat

## Kill current jobs
## Getting list of existent files with e.g. crab report -d scenarioA_mpi_1_mA_0p25_ctau_100/crab_scenarioA_mpi_1_mA_0p25_ctau_100/
### The total list of jobs is in scenarioA_mpi_1_mA_0p25_ctau_100/crab_scenarioA_mpi_1_mA_0p25_ctau_100/results/filesToProcess.json
### List of finished jobs is in scenarioA_mpi_1_mA_0p25_ctau_100/crab_scenarioA_mpi_1_mA_0p25_ctau_100/results/processedFiles.json
## Get list of missing files
## Add files to submission script
## Submit again
