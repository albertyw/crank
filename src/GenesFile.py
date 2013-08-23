"""
This manages File I/O for Gene Trees Files.  A Gene Trees File is a CSV
where each line contains a gene tree name, structure, and weight separated by
commas.

Weight should be used as the multiplier on the AnGST score

See FileCreation.py for how to create a Gene Trees File

Albert Wang
July 23, 2011
"""

import csv
import Tree

class GenesFile:
    """
    This class handles the reading of Gene Trees Files
    """
    def __init__(self, file_location):
        """
        File location refers to the location of the Gene Trees File to
        be read for Crank
        """
        self.file_location = file_location
        self.trees = []
        if self.file_location != '':
            self.parse_file()

    def parse_file(self):
        """
        This does the parsing of the actual file
        """
        csv_reader = csv.reader(open(self.file_location,'rb'), delimiter=',')
        for line in csv_reader:
            if line[0][0] == '#' or len(line[0]) == 0: # Comment in file
                continue
            tree = dict({})
            tree['name'] = line[0]
            tree['structure'] = line[1]
            tree['weight'] = float(line[2])
            tree['boots'] = [Tree.GeneTree(gene_tree) for gene_tree in line[3:]]
            self.trees.append(tree)

    def write_file(self, output_file):
        """
        This writes the GenesFile given the information currently in this instance
        """
        csv_writer = csv.writer(open(output_file,'wb'), delimiter=',')
        for tree in self.trees:
            row = [tree['name'], tree['structure'], tree['weight']]
            if tree['boots'] != []:
                row += [str(tree) for tree in tree['boots']]
            csv_writer.writerow(row)

    def select_trees(self, names_list):
        """
        Given a list of gene tree names, return a GenesFile with only
        those trees
        """
        selected_trees = []
        for tree in self.trees:
            if tree['name'] in names_list:
                selected_trees.append(tree)
        new_file = GenesFile('')
        new_file.trees = selected_trees
        return new_file

    def get_trees(self, cutoff = 0):
        """
        Returns a list of gene tree names in the GenesFile with a weight that is
        higher than the cutoff

        The output list should be compatible with the input for select_trees()
        """
        tree_names_list = []
        for tree in self.trees:
            if tree['weight'] > cutoff:
                tree_names_list.append(tree['name'])
        return tree_names_list

    def get_tree_by_name(self, tree_name):
        """
        Given a tree's name return the Gene Tree with that name
        """
        for tree in self.trees:
            if tree['name'] == tree_name:
                return tree
        return None
