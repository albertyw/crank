"""
This file takes a GenesFile and a species tree as arguments, runs the 
reconciliation on the current node/machine, and writes the output to a file.  

This is a shortcut for reconciling stuff
"""
import csv
import os
import sys
import time
sys.path.append('../')
sys.path.append(os.path.dirname(__file__)+'/../')
sys.path.append('/home/albertyw/crank/')

import Cog
import GenesFile
import Tree

# Read the arguments
if len(sys.argv) < 3:
    print 'argument 1: species tree location'
    print 'argument 2: genesfile location'
    print 'argument 3 (optional): output location'
    sys.exit()
species_tree_location = sys.argv[1]
gene_trees_location = sys.argv[2]
if len(sys.argv) > 3:
    output_file_location = sys.argv[3]
else:
    output_file_location = species_tree_location+'_output'

# Read the species tree
species_tree_handle = open(species_tree_location,'r')
species_tree = Tree.SpeciesTree(species_tree_handle.read())
species_tree_handle.close()

# Read the Genes File
gene_trees = GenesFile.GenesFile(gene_trees_location)
penalties = {'dup': 2, 'los': 1, 'hgt': 3, 'spc': 0}

# Reconcile
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
print 'Writing Output'
output_file_handle = csv.writer(open(output_file_location,'wb'),
    delimiter=',', quoting=csv.QUOTE_MINIMAL)
for cog in cog_list:
    output_file_handle.writerow([cog.name, cog.weight, cog.score, cog.weighted_score, cog.run_time, cog.events])



