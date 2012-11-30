#!/usr/bin/env python
# -*- coding: utf-8 -*-

# date of created : 081012
# date of modified : 301012
# - to put the parser argument 

import sys
import random
import argparse
from argparse import RawTextHelpFormatter
                 
def randomlyPickedLines(randRate, input_file):
   for line in input_file:
      # randomize at 0.02% at each line for bin of 300 bp
      # randomize at 0.2% at each line for bin of 3000 bp
      if random.random() < randRate:
         sys.stdout.write(line)

if __name__ == "__main__":
   # Build argument parser.
   parser = argparse.ArgumentParser(
         prog = 'randomlyPickedLines.py',
         description = """ picked lines randomly
         - input file is in bed
         - randomize at 0.02 for 300 bp and 
         - randomize at 0.2 for 3000 bp
          """,
         formatter_class=RawTextHelpFormatter
   )
   parser.add_argument(
         '-p',
         '--randRate',
         metavar = 'n',
         type = float,
         nargs = '?',
         default = 0.02,
         help = 'The rate to randomize at each line for binning'
   )
   parser.add_argument(
         'input_file',
         metavar = 'f',
         type = file,
         nargs = '?',
         default = sys.stdin,
         help = 'file to process'
   )
 
   args = parser.parse_args()
   randomlyPickedLines(args.randRate, args.input_file)
