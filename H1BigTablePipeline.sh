#/bin/sh 
#date of birth : 091012

################################################################################
# Pipe line to combine all the files assembled with similar reference genome   #
# into one big table (with ca. 200,000 lines,randomly picked)                  #
# *files are in the bed format*                                                #                           
################################################################################

#for safety
trap 'echo Keyboard interruption... ; exit 1' SIGINT

if [ $# -eq 0 ]; then
  echo "Usage:H1BigTablePipeline.sh -r [n]-i [input files] -o [output]"
  echo "e.g ./H1BigTablePipeline.sh -r 0.2 -i 'TEST/*' -o TEST/bigTable.bed"
  echo "-r [n] 0.2 for 3000bp and 0.02 for 300bp"
exit 1
fi

while getopts ":r:i:o:" opt; do
  case $opt in
    r)
      echo "-r randomize rate for each line: $OPTARG" >&2
      randRate="$OPTARG"
      ;;
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

#remove the lines where all the reads of all the columns for each line are zeros
Nonzero_file="NonZero-"$mapped_file
./removeZero.py $dir/$mapped_file > $dir/$Nonzero_file

#randomly picked lines, randomize at 0.02% of the total line from the file
Randomlypicked_file="RandomlyPicked-"$Nonzero_file
./randomlyPickedLines.py -p "$randRate" $dir/$Nonzero_file > $dir/$Randomlypicked_file

#add the header to the randomized file
#1. check if the no.of columns is equal between the header file(Nonzero_file) and Randomlypicked_file
col1=$(awk -F'\t' '{print NF; exit}' $dir/$Randomlypicked_file)
col2=$(awk -F'\t' '{print NF; exit}' $dir/$Nonzero_file)
if [ $col1 = $col2 ]; then
  #get the header
  head -1 $dir/$Nonzero_file > $dir/header.txt
  #put the header together 
  cat $dir/$Randomlypicked_file >> $dir/header.txt
  #rename the file         
  mv $dir/header.txt $output
  else
    echo "the columns are not equal when trying to add the header"
    exit 1
fi
