#!/usr/bin/env python
# -*- coding:utf-8 -*-
#date: 291012

########################################################
# Check files that contain all the reads that are zero #
########################################################

import sys
import argparse
from argparse import RawTextHelpFormatter

def checkRead(input_file):
   """
   Check if in all lines the reads are zero and 
   write the input filename if it's the case
   """
   count_zero = 0
   line_no = 0
   for line in input_file:
      items = line.split('\t')
      read = int(items[3])
      line_no += 1
      if read == 0:
         count_zero += 1
   if count_zero == line_no:
      sys.stdout.write(input_file.name + '\n')

if __name__ == "__main__":
   parser = argparse.ArgumentParser(
         prog = 'CheckRead.py',
         description =  """Check if the sam file contains only zero reads,
         output: the list of files that contain reads with only zero""",
         formatter_class=RawTextHelpFormatter
   )
   parser.add_argument(
         'input_file',
         metavar = 'f',
         type = file,
         nargs = '*',
         default = sys.stdin,
         help = 'file to check'
   )
   args = parser.parse_args()

   #run checking for a list of files
   for i_file in args.input_file:
      checkRead(i_file)

