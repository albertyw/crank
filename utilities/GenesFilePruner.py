"""
This program reads a GenesFile, selects gene trees that follow a certain 
condition, then saves those gene trees into a different GenesFile

"""
import sys

sys.path.append('/home/albertyw/crank/src/')
import Tree
import GenesFile

if len(sys.argv) < 2:
    print 'Argument 1: original genesfile'
    print 'Argument 2: new genesfile'

original_genes_file = sys.argv[1]
new_genes_file = sys.argv[2]

ribosomal_cogs = ['arCOG06624', 'arCOG04057', 'arCOG04304', 'arCOG01220', 'arCOG04327', 'arCOG04305', 'arCOG04293', 'arCOG04287', 'arCOG04168', 'arCOG04167', 'arCOG04175', 'arCOG04097', 'arCOG01752', 'arCOG04183', 'arCOG01946', 'arCOG04314', 'arCOG04177', 'arCOG04126', 'arCOG01950', 'arCOG00781', 'arCOG04094', 'arCOG04473', 'arCOG04245', 'arCOG04096', 'arCOG04240', 'arCOG04088', 'arCOG00782', 'arCOG04113', 'arCOG04208', 'arCOG01751', 'arCOG04182', 'arCOG01885', 'arCOG04108', 'arCOG01722', 'arCOG04242', 'arCOG04129', 'arCOG04288', 'arCOG04209', 'arCOG00785', 'arCOG01344', 'arCOG04243', 'arCOG04255', 'arCOG04372', 'arCOG04093', 'arCOG04109', 'arCOG04098', 'arCOG04089', 'arCOG04154', 'arCOG04067', 'arCOG04049', 'arCOG04086', 'arCOG04087', 'arCOG04186', 'arCOG00780', 'arCOG04185', 'arCOG04254', 'arCOG04071', 'arCOG04070', 'arCOG04072', 'arCOG04099', 'arCOG00779', 'arCOG04095', 'arCOG04092', 'arCOG04091', 'arCOG04090', 'arCOG04239', 'arCOG04289', 'arCOG01758']

# Modify the gene tree
genes_file = GenesFile.GenesFile(original_genes_file)
tree_id = len(genes_file.trees)-1
while tree_id >= 0:
    if tree_id % 16 != 0:
        genes_file.trees.pop(tree_id)
    tree_id -=1
"""
tree_id = 0
while tree_id < len(genes_file.trees):
    #print tree_id
    tree = genes_file.trees[tree_id]
    # Remove genes that follow this if statement  - CHANGE THIS
    leaves = Tree.GeneTree(tree['structure']).ete.get_leaf_names()
    if len(leaves) != 69 or len(set(leaves)) != 69:
        genes_file.trees.pop(tree_id)
        continue
    # Take only arcogs in array
    #if tree['name'] not in ribosomal_cogs:
    #    genes_file.trees.pop(tree_id)
    #    continue
    genes_file.trees[tree_id] = tree
    
    tree_id += 1
"""
# Save the gene tree
genes_file.write_file(new_genes_file)

print 'Wrote ', len(genes_file.trees), ' Trees'
