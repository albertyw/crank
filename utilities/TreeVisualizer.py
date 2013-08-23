"""
This file reads a tree file and then makes images of the tree
"""

import os, shutil, sys, tempfile

sys.path.append('/home/albertyw/crank/src/')
import Tree

sys.path.append('../../itol')
sys.path.append(os.path.dirname(__file__)+'/../../itol')
import Itol, ItolExport


class TreeVisualizer:
    def __init__(self, tree_location):
        self.tree_location = tree_location

    def make_trees(self):
        """
        Create trees from the base.tree outputs
        """
        csv_files = dict({})
        csv_files['/home/albertyw/tester/output/archaeal_groups.csv'] = 'groups'
        csv_files['/home/albertyw/tester/output/archaeal_phyla.csv'] = 'phyla'
        tree_handle = open(self.tree_location,'r')
        tree_string = tree_handle.read()
        tree_handle.close()
        tree = Tree.SpeciesTree(tree_string)

        # Make the original tree
        self.write_tree(tree, self.tree_location+'.pdf')
        print self.tree_location+'.pdf'

        # Make the trees with renamed leaves
        for file_location in csv_files.keys():
            renamed_tree = tree.rename_leaves(csv_file=file_location)
            self.write_tree(renamed_tree, self.tree_location+'_'+str(csv_files[file_location])+'.pdf')
            print self.tree_location+'_'+str(csv_files[file_location])+'.pdf'

    def write_tree(self, tree, save_location):
        """
        Given a tree, render the tree using Itol and save to the save_location
        """
        # Format tree structure
        tree_structure = tree.tree_structure
        tree_structure = tree_structure.replace('>','')

        # Write tree structure to a tempfile
        temp = tempfile.NamedTemporaryFile()
        temp.write(tree_structure)
        temp.seek(0)
        temp.flush()

        # Upload to itol
        itol = Itol.Itol()
        itol.add_variable('treeFile',temp.name)
        itol.add_variable('treeName','asdf')
        itol.add_variable('treeFormat','newick')
        good_upload = itol.upload()
        if good_upload == False:
            print
            print 'ERROR:'+save_location
            print itol.comm.upload_output
            print
            return

        # Download from itol
        itol_exporter = itol.get_itol_export()
        itol_exporter.set_export_param_value('format','pdf')
        itol_exporter.set_export_param_value('ignoreBRL','1')
        itol_exporter.set_export_param_value('displayMode','normal')
        itol_exporter.set_export_param_value('fontSize','20')
        itol_exporter.export(save_location)
        temp.close()

if __name__ == "__main__":
    tree_location = sys.argv[1]
    viz = TreeVisualiser(tree_location)
    viz.make_trees()


