# List datasets in DAS:
dasgoclient --query="dataset=/*/tafoyava*_2023-*/* instance=prod/phys03" > files.txt

# Invalidate all files in the datasets listed in "files.txt":
while read p; do
	crab-dev setfilestatus --status INVALID --dataset ${p}
	#crab-dev setfilestatus --status INVALID --dataset ${p} & # this parallelises the crab job, useful since it usually takes some time due to latency
done < files.txt

# Invalidate all the datasets (not the files) listed in "files.txt":
while read p; do
	crab-dev setdatasetstatus --status INVALID --dataset ${p}
done < files.txt

# N.B. if you re-send production, samples will likely keep the same signature (the jumble of characters e.g. tafoyava-scenarioA_mpi_10_mA_1p00_ctau_0p1_2023-622dffdc6a3cfe7c99a725908eb67d1a/USER
# if you want to restart a production, you have to
#	- invalidate all files within a dataset
#	- leave the datasets as valid
# regenerate






# To trim out the end of each line after a string (in this case, it's looking for "-scenario"), you can use

sed -E 's/(-scenario).*".*/\1"/' dictionary_gen.txt > dictionary_gen.txt_trimmed
