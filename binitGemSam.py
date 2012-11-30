#!/usr/bin/env python
# -*- coding:utf-8 -*-

# date created : 130912
# date modified : 280912 
#  - modified to add new feature that can bin bed file
# date modified: 231012
#  - modified the input_file argument to allow the list of files as input
#  - modified to allow multiple threading
# date modified: 291012
#  - modified to handle the tab FS(Field Separator) of sam formatted file
# date modified: 061112
#  - modified to change multiple threading module with multiprocessing 
# date modified: 281112
#  - modified to skip the header line started with @


##########################################################################################
# Bin the alignment file generated by gem mapper(gem-2-sam), index starts with 1         #
# Bin's index is the alignment coordinate/bin size                                       #
# Assembly used by default is hg19 in a dict form                                        #
##########################################################################################

#default dict use for counting
from collections import defaultdict

#for I/O and commandline parsing
import os
import sys
import argparse
from argparse import RawTextHelpFormatter
import glob
import gc
import errno

# for threading jobs
import multiprocessing
import Queue

# default assembly: hg19 reference genome
# key:chr and value: size
dict_genome_size_hg19 = {
   'chr1': 249250621,
   'chr2': 243199373,
   'chr3': 198022430,
   'chr4': 191154276,
   'chr5': 180915260,
   'chr6': 171115067,
   'chr7': 159138663,
   'chr8': 146364022,
   'chr9': 141213431,
   'chr10': 135534747,
   'chr11': 135006516,
   'chr12': 133851895,
   'chr13': 115169878,
   'chr14': 107349540,
   'chr15': 102531392,
   'chr16': 90354753,
   'chr17': 81195210,
   'chr18': 78077248,
   'chr19': 59128983,
   'chr20': 63025520,
   'chr21': 48129895,
   'chr22': 51304566,
   'chrX': 155270560,
   'chrY': 59373566,
}

def dict_GenomeSize(input_file):
   """
   create a dictionary
   - key: chromosomes in the genome
   - value: size 
   """
   with open(input_file) as f:
      # Assume no header.
      # Assume 2 items per line!!
      return dict([line.split() for line in f])

def binit(bin_size, input_file, format='sam', dict_hg19 = dict_genome_size_hg19, output_dir='.'):
   """binning the coordinate of the alignment"""

   # key: (chromosome, bin index)
   # value: no of reads
   freq_table = defaultdict(int)

   if format == 'bed':
      chrom_field = 0
      start_field = 1
   else:
      # Default sam format
      chrom_field = 2
      start_field = 3

   try:
      with open(input_file, 'r') as in_f:
         for line in in_f:
            header=line[0]
            if header == "@":
               continue
            else:
               items = line.split('\t')
               #bin only chromosomes that are in the dict_hg19
               if items[start_field] != '*' and items[chrom_field] in dict_hg19:
                  freq_table[(items[chrom_field],int(items[start_field])/bin_size)] += 1
               else:
                  continue

   except IndexError:
      sys.stderr.write("Check if your file is properly formatted, !field separator is a tab!")
   except:
      sys.stderr.write('file error:%s'%(in_f.name))
      raise


   #collect all the aligned chromosome without duplicates 
   chroms = set([chrom for (chrom,bin) in freq_table.keys()])

   #start binning ...

   # remove the garbage collector during list append
   gc.disable()

   bin_list=[]
   for chrom in sorted(dict_hg19):
      chrom_size = int(dict_hg19[chrom])
      maxbin = int(chrom_size/bin_size)
      for bin in range(maxbin):
         bin_list.append("%s\t%s\t%s\t%d\n" % \
                     (chrom, 1+bin*bin_size,
                           (1+bin)*bin_size, freq_table[(chrom,bin)]))

   gc.enable()

   #finally output the file                                     
   if not os.path.exists(output_dir):
      try:
         os.makedirs(output_dir)
      except OSError as exception:
         if exception.errno != errno.EEXIST:
            raise

   head, tail = os.path.split(input_file)
   base = os.path.splitext(tail)[0]
   output_fname="%sbin-%s.bed" %(bin_size,base)
   output_file = str(os.path.join(output_dir, output_fname))

   with open(output_file, 'w') as output_f:
      for line in bin_list:
         output_f.write(line)

class binThread (multiprocessing.Process):
   """
   Binning in threads
   """
   def __init__(self, lock, queue, bin_size, output_dir):
      self.lock = lock
      self.queue = queue
      self.bin_size = bin_size
      self.output_dir = output_dir
      multiprocessing.Process.__init__(self)

   def run(self):
      while True:
         # Wait for data in task queue.
         self.lock.acquire()
         try:
            input_f = queue.get_nowait()
         except Queue.Empty:
            # finish
            return
         finally:
            self.lock.release()

         binit(bin_size=self.bin_size, output_dir=self.output_dir, input_file=input_f)
         self.queue.task_done()


if __name__ == "__main__":
   # Build argument parser.
   parser = argparse.ArgumentParser(
         prog = 'binitGemSam.py',
         description = """ Binning the aligment file in 300bp(default bin size):
         - default format is sam
           - sam files obtained by gem-2-sam
         - optional format is in bed 
         - n: number of cores for multiprocessing
         !NOTE this program requires a big chunk of memory, the binning dumped directly into memory to speed up the binning!""",
         formatter_class=RawTextHelpFormatter
   )
   parser.add_argument(
         '-b',
         '--bin-size',
         metavar = 'n',
         type = int,
         nargs = '?',
         default = 300,
         help = 'bin size in base pairs'
   )
   parser.add_argument(
         '-fmt',
         '--format',
         metavar = 'fmt',
         type = str,
         nargs = '?',
         default = 'sam',
         help = 'format of the input file'
   )
   parser.add_argument(
         '-n',
         '--n-threads',
         metavar = 't',
         type = int,
         nargs = '?',
         default = 1,
         help = 'number of threads to run in parallel'
   )
   parser.add_argument(
         '-od',
         '--output_dir',
         metavar = 'od',
         type = str,
         nargs = '?',
         default = '.',
         help = 'directory for the output file'
   )
   parser.add_argument(
         'input_file',
         metavar = 'f',
         type = str,
         nargs = '?',
         default = sys.stdin,
         help = 'file to process'
   )

   args = parser.parse_args()


   # bin with threads
   lock = multiprocessing.Lock()
   queue = multiprocessing.JoinableQueue(-1) #no.limit for queue
   manager = multiprocessing.Manager()


   # Fill in task queue while threads are running.
   for f_task in glob.glob(args.input_file):
      queue.put_nowait(f_task)

   # Create and start binning in threads.
   threads = [binThread(lock, queue, args.bin_size, args.output_dir) for i in range(args.n_threads)]
   for thread in threads:
      thread.start()
   queue.join()
