#/bin/sh 
#date created: 191012

#extract all the .fastq files from the .tgz files

trap 'echo Keyboard interruption... ; exit 1' SIGINT

for fastq in $(ls *.tgz)
do                                                                     
  echo "currently processing $fastq"
  #grep the list of fastq files
  tar tvfz "$fastq" --wildcards '*/*.fastq' | awk '{print $6}' > tmp && echo "Listing File OK" >&2;
  #start extracting the list of files
  for i in $(cat tmp)
  do
    tar xzf "$fastq" "$i" -C . && echo "Extracting file OK" >&2;
    f_name="$fastq-$(basename $i)" 
    mv "$i" ./"$f_name"
  done
done                           

