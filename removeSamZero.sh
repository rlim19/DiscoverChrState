#/bin/sh 

# date : 291012

##################################################
# Remove files that contain reads with only zero #
# files contain in the list as a text file       #
##################################################


for i in $(cat $1)
do
  echo "removing file $i"
  rm $i
done
