"""
This script is used to create the Gene Trees File for Crank.  Because it is much
slower for Crank to read a separate file for each gene tree, this program
compiles all gene trees into one file, and also adds metadata to go with the
trees.  By default, this program uses the file name as the gene tree name, and
a constant value "1" for the weight.

Gene Trees File Format:
Gene Tree Name, Gene Tree Structure, Gene Tree Score Weight

Argument 1: The directory that has the gene trees

Albert Wang
June 1, 2011

TODO: Change weight from being a constant "1"
"""

import csv
import re
import sys
import os
sys.path.append('/home/albertyw/crank/src/')
from Tree import GeneTree

# Read arguments
gene_tree_directory = sys.argv[1]+'/'

# Get a list of gene trees
file_names = os.listdir(gene_tree_directory)
file_names.sort()
#file_names = [gene_tree_directory+file_name for file_name in file_names]
gene_trees = []
for file_name in file_names:
    if file_name+'.boots' in file_names:
        file_names.remove(file_name+'.boots')
        gene_trees.append((file_name,file_name+'.boots'))
    else:
        gene_trees.append((file_name,))

# Create the csv and write to the output file
csv_writer = csv.writer(sys.stdout, delimiter=',',
    quoting=csv.QUOTE_MINIMAL)
i = 0
while i < len(gene_trees):
    gene_tree_name = gene_trees[i][0]
    gene_tree_handle = open(gene_tree_directory + gene_tree_name, 'r')
    gene_tree = gene_tree_handle.read().strip()
    gene_tree_handle.close()

    ## HACK
    gene_tree_name = gene_tree_name[0:-21]
    ## END HACK

    gene_tree = re.sub('_[0-9]*','',gene_tree)

    if len(gene_trees[i]) > 1:
        boot_tree_name = gene_trees[i][1]
        boot_tree_handle = open(gene_tree_directory + boot_tree_name,'r')
        boot_trees = boot_tree_handle.readlines()
        boot_tree_handle.close()
        boot_trees = [boot_tree.strip() for boot_tree in boot_trees]
    else:
        boot_trees = []

    if len(gene_tree) == 0:
        i += 1
        continue
    gene_tree = GeneTree(gene_tree)
    weight = str(gene_tree.calculate_weight())

    csv_writer.writerow([file_names[i], str(gene_tree), weight]+boot_trees)
    i += 1


