"""
This file reads a genes file and turns each gene tree into an image
"""

import csv
import os
import sys
import tempfile

sys.path.append('/home/albertyw/crank/src/')
from GenesFile import GenesFile
import Tree

sys.path.append('../../itol')
sys.path.append(os.path.dirname(__file__)+'/../../itol')
import Itol, ItolExport

def make_tree_image(gene_tree, gene_tree_name, output_directory):
    """
    Given a tree, save the tree using Itol to the save_location
    """
    # Format tree structure
    gene_tree = gene_tree.standardize_sister_ordering()
    tree_structure = gene_tree.standardize_leaf_names()
    
    # Write tree structure to tempfile
    temp = tempfile.NamedTemporaryFile()
    temp.write(tree_structure)
    temp.seek(0)
    temp.flush()
    
    # Upload to itol
    itol = Itol.Itol()
    itol.add_variable('treeFile',temp.name)
    itol.add_variable('treeName', gene_tree_name)
    itol.add_variable('treeFormat', 'newick')
    good_upload = itol.upload()
    if good_upload == False:
        print
        print 'ERROR:'+save_location
        print itol.comm.upload_output
        print
        return
        
    # Download from itol
    itol_exporter = itol.get_itol_export()
    itol_exporter.set_export_param_value('format','png')
    itol_exporter.set_export_param_value('ignoreBRL','1')
    itol_exporter.set_export_param_value('displayMode','normal')
    itol_exporter.set_export_param_value('fontSize','20')
    itol_exporter.export(output_directory+gene_tree_name+'.png')
    temp.close()
    print output_directory+gene_tree_name+'.png'


genes_file_location = sys.argv[1]
output_directory = sys.argv[2]+'/'
csv_files = dict({})
csv_files['/home/albertyw/tester/output/archaeal_groups.csv'] = 'groups'
csv_files['/home/albertyw/tester/output/archaeal_phyla.csv'] = 'phyla'


genes_file = GenesFile(genes_file_location)

for tree in genes_file.trees:
    tree_name = tree['name']
    tree = Tree.GeneTree(tree['structure'])
    # Make original tree
    make_tree_image(tree, tree_name, output_directory)
    # Make trees with rewritten leaves
    for file_location in csv_files.keys():
        renamed_tree = tree.rename_leaves(csv_file=file_location)
        make_tree_image(renamed_tree, tree_name+str(csv_files[file_location]), output_directory)
    
