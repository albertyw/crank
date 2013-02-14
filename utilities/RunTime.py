"""
This file reads the output of a reconciliation and finds the total time
"""

import csv
import sys

# Find where the location of the reconciliation output
output_file_location = sys.argv[1]

# Read the reconciliation output
output_file_handle = csv.reader(open(output_file_location, 'rb'), \
    delimiter=',', quoting=csv.QUOTE_MINIMAL)
time = 0.0
for line in output_file_handle:
    time += float(line[4])

print 'Total Time: '+str(time)+' sec - '+str(time/60)+' min'
