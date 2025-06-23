# Recurrent surveillance can look like this

cd /home/hep/jtafoyav/production_2023/tools/status_smarter/AODSIM

while true; do python3 status_A.py -r; echo " "; echo " "; echo " "; echo " "; echo " "; echo "Cleaning crab output files";
cd /home/hep/jtafoyav/production_2023/CMSSW_13_0_14/src/2023_AOD-ext/; pwd; for DIR in scenario*; do rm -f ${DIR}/crab_${DIR}/crab.log ;
touch ${DIR}/crab_${DIR}/crab.log ; done; cd -; echo " "; echo " "; sleep 5h; done
