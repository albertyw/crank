#! /usr/bin/python -O
"""
This file is the file that is actually submitted to cluster job queue.  
This should be coupled with an input file and be run as:
$ python Job.py input

The input.file should be formatted as:
species tree location: the location of the species tree to be reconciled
gene tree location: the location of the GenesFile tree to be reconciled
selected trees: A list of the trees' names that you want to run
penalties location
output file location

The output.file should be formatted as:
Tree Name: The name of the tree from the GenesFile/selected trees list
Cog Weight: The weight of the tree, from the GenesFile
Cog Score: The score that AnGST gave for the reconciliation
Cog run_time: The time that it took the Cog/Tree to run
Cog Events: A list of events that is needed for the Cog Events  

Albert Wang
December 28, 2010
"""
import csv
import sys
import time

import GenesFile
import Tree
import Cog

# Open the job info file
info_file_location = sys.argv[1]
info_file_handle = open(info_file_location,'r')
info_file = info_file_handle.readlines()
info_file_handle.close()

species_tree = Tree.SpeciesTree(info_file[0].strip())
species_tree = species_tree.standardize_sister_ordering()
gene_trees_location = info_file[1].strip()
selected_trees = eval(info_file[2].strip())
penalties = eval(info_file[3].strip())
output_file_location = info_file[4].strip()

# Read gene_trees
gene_trees = GenesFile.GenesFile(gene_trees_location)
# Load selected gene trees into Cog.py
gene_trees = gene_trees.select_trees(selected_trees)

# Run Cog.py
cog_list = [0]*len(gene_trees.trees)
i = 0
while i < len(gene_trees.trees):
    start_time = time.time()
    tree = gene_trees.trees[i]
    new_cog = Cog.Cog(species_tree, tree, penalties)
    new_cog.reconcile()
    new_cog.run_time = time.time() - start_time
    cog_list[i] = new_cog
    i += 1

# Save data into output file
output_file_handle = csv.writer(open(output_file_location,'wb'),
    delimiter=',', quoting=csv.QUOTE_MINIMAL)
for cog in cog_list:
    output_file_handle.writerow([cog.name, cog.weight, cog.score, cog.weighted_score, cog.run_time, cog.events])

