#/bin/sh -i
#date of birth : 091012

################################################################################
# Pipe line to combine all the files assembled with similar reference genome   #
# into one big table                                                           #
################################################################################

#for safety
trap 'echo Keyboard interruption... ; exit 1' SIGINT

if [ $# -eq 0 ]; then
  echo "Usage:H1BigTablePipeline.sh -i [input files] -o [output]"
  echo "e.g ./H1BigTablePipeline.sh -i 'TEST/*' -o TEST/bigTable.bed"
exit 1
fi

while getopts ":i:o:" opt; do
  case $opt in
    i)
      echo "-i your input files are: $OPTARG" >&2
      input="$OPTARG"
      ;;
    o)
      echo "-o your output file is stored: $OPTARG" >&2
      output="$OPTARG"
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


input_files=$(ls $input)
#get only the file without the output di
output_file=${output##*/};
merged_file="merged-"$output_file
dir=$(dirname "$output")         

#start merging
./mergeBed.py $input_files > $dir/$merged_file 

#pick randomfiles for coordinate

#1.count the total number of input files
no_inputFiles=$(echo $input_files | awk '{print NF}')
#2.shuffle from 1 to the total number
random_noFiles=$(shuf -i 1-$no_inputFiles -n 1)
#make an array containing all the input files
arr_input=($input_files)
randomFiles=${arr_input[$random_noFiles]} #This is the picked randomFiles
echo "The used file for coordinate: $randomFiles"

#get the coordinates
awk -v OFS='\t' '{print $1, $2, $3}' $randomFiles | awk 'BEGIN{print "chr\tstart\tend"}1' > $dir/coordinates.txt

#combine the merged files with the coordinates file
mapped_file="mapped-"$merged_file
paste $dir/coordinates.txt $dir/$merged_file > $dir/$mapped_file

#get the header_file
head -1 $dir/$mapped_file > $dir/header.txt

#put the header together
cat $dir/$mapped_file >> $dir/header.txt

#rename the file
mv $dir/header.txt $output
