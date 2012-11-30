#!/usr/bin/env python
# -*- coding:utf-8 -*-

#################################################################
# Count the number of mismatches and matches in a combined file #
# The combined file: cat file1 file2                            #
#################################################################

from __future__ import division
import sys
from collections import defaultdict


counter = defaultdict(int)
with open(sys.argv[1]) as f:
   for line in f:
      counter[line] +=1

mismatches = 0
matches = 0
for key in counter:
   if counter[key] == 1:
      mismatches += 1
   else:
      matches += 1

print "mismatches:%d\nmatches:%d\nratio Match/MisMatch:%0.2f" %(mismatches, matches, matches/mismatches)
