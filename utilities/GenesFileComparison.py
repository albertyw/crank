"""
This file reads two genes files and compares the gene trees in both
"""

import csv
import sys
sys.path.append('/home/albertyw/crank')
from GenesFile import GenesFile
import Tree

if len(sys.argv) < 3:
    print "python GenesFileComparison.py GenesFile1 GenesFile2"
    sys.exit()

genes_file_1_location = sys.argv[1]
genes_file_2_location = sys.argv[2]
genes_file_1 = GenesFile(genes_file_1_location)
genes_file_2 = GenesFile(genes_file_2_location)

print "Total trees in "+genes_file_1_location+": "+str(len(genes_file_1.trees))
print "Total trees in "+genes_file_2_location+": "+str(len(genes_file_2.trees))

rf_scores = []
comparisons = 1
for tree_1 in genes_file_1.trees:
    tree_name = tree_1['name']
    # <hack>
    tree_name = tree_name[0:-6] + '.fasta_phyml_tree.txt'
    # </hack>
    tree_2 = genes_file_2.get_tree_by_name(tree_name)
    if tree_2 == None:
        continue
    tree_1_object = Tree.Tree(tree_1['structure'])
    tree_2_object = Tree.Tree(tree_2['structure'])
    score = tree_1_object.robinson_foulds(tree_2_object)
    print tree_1['name'] + ' : ' + str(score)
    rf_scores.append(score)
    comparisons += 1

rf_scores.sort()
print "Average Robinson-Foulds score is: "+str(sum(rf_scores) / comparisons)
print "Median Robinson-Foulds score is: "+str(rf_scores[len(rf_scores)/2])
print "Max score is: "+str(rf_scores[-1])
print "Min score is: "+str(rf_scores[0])
print 'Total number of compared trees: '+str(comparisons-1)



