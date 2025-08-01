# Enable proxy
voms-proxy-init --rfc --voms cms -valid 192:00


# Get a list of all the samples complying with the naming convention:
dasgoclient --query="dataset=/*/tafoyava*_GENSIM_2023_post*/* instance=prod/phys03" > datasets_GENSIM_postBPix.txt


# Retrieve details of each of the samples
rm results_GENSIM_postBPix.txt
while read p; do
    echo "$p"
    echo "$p" >> results_GENSIM_postBPix.txt
    echo "$( dasgoclient --query="summary dataset=$p instance=prod/phys03" )" >> results_GENSIM_postBPix.txt
    sleep 2
done <datasets_GENSIM_postBPix.txt


# Make a dictionary out of the results_GENSIM_postBPix.txt file
Use `results_makedictionary.py'


# Summarise the results stored in results_GENSIM_postBPix.txt (i.e. simply get sample)
Use `results_manage.py'



# Make a loop for constant monitoring with e.g.
while true; do ./list_datasets.sh GENSIM_2023-v2_ext;
	FILE="results_GENSIM_2023-v2_ext.txt";
	python3 results_manage.py output/${FILE};
	cp output/${FILE}_formated /home/hep/jtafoyav/public_html/dqcd-production-status/2023/${FILE};
	echo " "; echo " "; echo " "; echo " "; echo " "; echo " "; date; echo "Waiting 2h"; sleep 2h; done

# Used to monitor the GEN level intermediate mass samples
while true; do ./list_datasets.sh "2023_postBPix-ext"; FILE="results_GENall_2023_postBPix-ext.txt"; python3 results_manage.py output/${FILE}; cp output/${FILE}_formated /home/hep/jtafoyav/public_html/dqcd-production-status/2023/${FILE}_includingIntermediateMasses; echo " "; echo " "; echo " "; echo " "; echo " "; echo " "; date; echo "Waiting 2h"; sleep 2h; done
