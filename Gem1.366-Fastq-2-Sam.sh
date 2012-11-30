#/bin/sh 

#################################
# Convert fastq to SAM with GEM #
# !gem_version 1.366!           # 
#################################

usage()
{
if [ $# -eq 0 ];then
  echo "Usage: $0 -n [no.core] -i [fastq_file] -o [output_dir]"
  echo "[output_dir]: storage directory !create this dir in advance!"
  echo "[no.core]: for threading"
  exit 1
fi
}

usage "$@"

while getopts ":i:n:o:" opt; do
  case $opt in
    i)
      echo "-i your input fastq file is $OPTARG" >&2
      input_f="$OPTARG"
      ;;
    n)
      echo "-n number of cores uses: $OPTARG" >&2
      core="$OPTARG"
      ;;
    o)
      echo -e "-o output directory: $OPTARG\n" >&2
      output_dir="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1                                          
      ;;
  esac
done

#mapping...
echo "Gem mapping of $input_f" >&2;        
gem-mapper -I 'hg19_1.366/hg19.gem' -i $input_f -q 'offset-33' -o $output_dir/$input_f -t $core && echo "OK" >&2;
#combine all the maps into one file
map_f=$input_f.map

#check the file_size of the mapped_file
file_size=$(stat -c %s $output_dir/$map_f)
if [[ $file_size -ne 0 ]]; then
  #convert to sam file
  echo "Sam conversion of $input_f" >&2;
  sam_f=$input_f.sam
  gem-2-sam -i $output_dir/$map_f -o $output_dir/$sam_f && echo "OK" >&2;
else
  echo "Sam conversion of $input_f: NOT OK" >&2
fi
