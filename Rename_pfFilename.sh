#bin/sh 
#date: 221012

#rename the long filename _pf.fastq with the short name (reference-ref.genome-number's identifier)
#e.g 
# hg19-H1-194.fastq.tgz-hES_JunD_sequence_rep2_110425_COLUMBO_00076_FC64E09_L1_pf.fastq changed into
# hg19-H1-194.fastq

#get all the long file_name
for pf_file in $(ls -l *pf.fastq | awk '{print $9}')
do
  #get the shortname
  short_name=$(echo $pf_file | cut -c 1-17)
  #rename it...
  mv $pf_file $short_name 
done
