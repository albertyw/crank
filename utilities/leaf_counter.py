"""
This file reads a GenesFile and creates a CSV counting the number of leaves
"""

import csv
import operator
import sys
sys.path.append('/home/albertyw/crank/utilities')
from GenesFileAnnotator import AnnotateGenesFile

genes_file_input_location = "/home/albertyw/greg/ribosomalGenesFileAnnotated"
csv_output_location = "leaf_counts.csv"

# Get a list of all leaves
leaves = dict({})
leaf_handle = csv.reader(open('/home/albertyw/tester/output/archaeal_species.csv','rb'))
for row in leaf_handle:
    leaves[row[0]] = row[1]

# Count leaves
leaf_count = dict({})
genes_file = AnnotateGenesFile(genes_file_input_location)
for tree in genes_file.trees:
    tree_leaves = tree['tree'].ete.get_leaf_names()
    leaf_count[tree['name']] = dict({})
    for leaf in leaves.keys():
        leaf_count[tree['name']][leaf] = 0
    for leaf in tree_leaves:
        leaf_count[tree['name']][leaf] += 1
    leaf_count[tree['name']]['tree_name'] = tree['annotation']



# Create CSV file
# Arcog#, familyname, species...., total
leaves_ids = leaves.keys()
leaves_ids.sort()
csv_lines = []
for tree_name, tree_leaves in leaf_count.items():
    line = [tree_name, tree_leaves['tree_name']]
    line += [tree_leaves[leaf] for leaf in leaves]
    line += [sum(line[2:])]
    csv_lines.append(line)
    
csv_writer = csv.writer(open(csv_output_location,'wb'))
csv_writer.writerow(["arCOG", "Name"]+leaves_ids+["Total"])
csv_lines.sort(key=operator.itemgetter(1))
for line in csv_lines:
    csv_writer.writerow(line)

