#/bin/sh 

#############################################
# extract binary fastq files into raw fastq #
#############################################

trap 'echo Keyboard interruption... ; exit 1' SIGINT

for fasq_f in $(ls .)
do
  if [[ ${fasq_f: -6} = ".fastq" ]]
  then
    echo "currently unpacking binary $fasq_f with.fastq"
    # add the .gz extension                  
    mv "$fasq_f" "$fasq_f".gz;
    gunzip "$fasq_f".gz
  
  elif [[ ${fasq_f: -3} == ".gz" ]]
  then
    echo "currently unpacking $fasq_f with .gz"
    gunzip "$fasq_f"
  fi
done
