"""
This file reads a genes file and annotates trees
"""

import csv
import sys
sys.path.append('/home/albertyw/crank')
from GenesFile import GenesFile
import Tree


class AnnotateGenesFile(GenesFile):
    def parse_file(self):
        """
        This does the parsing of the actual file
        """
        csv_reader = csv.reader(open(self.file_location,'rb'), delimiter=',')
        tree = dict({})
        for line in csv_reader:
            if line[0][0] == '#' or len(line[0]) == 0: # Comment in file
                tree['annotation'] = line[0][1:]
                continue
            tree['name'] = line[0]
            tree['structure'] = line[1]
            tree['weight'] = float(line[2])
            tree['boots'] = [Tree.GeneTree(gene_tree) for gene_tree in line[3:]]
            self.trees.append(tree)
            tree = dict({})
        
    def write_file(self, output_file):
        """
        This writes the GenesFile with the annotation information
        """
        csv_writer = csv.writer(open(output_file,'wb'), delimiter=',')
        for tree in self.trees:
            row = [tree['name'], tree['structure'], tree['weight']]
            if tree['boots'] != []:
                row += [str(tree) for tree in tree['boots']]
            if tree.has_key('annotation'):
                annotation = tree['annotation']
            else:
                annotation = ''
            annotation = annotation.replace(',', '\,')
            csv_writer.writerow(['#'+annotation])
            csv_writer.writerow(row)





if __name__ == "__main__":
    genes_file_input_location = sys.argv[1]
    family_descriptions_location = sys.argv[2]
    genes_file_output_location = sys.argv[3]
    
    arcog_location = 'arCOG.csv'
    
    # Create annotation dictionary
    descriptions = csv.reader(open(family_descriptions_location,'rb'), delimiter="\t")
    annotation = dict({})
    for row in descriptions:
        annotation[row[0]] = row[1]
    
    
    
    genes_file = AnnotateGenesFile(genes_file_input_location)
    for tree in genes_file.trees:
        if tree['name'] in annotation.keys():
            tree['annotation'] = annotation[tree['name']]
    
    genes_file.write_file(genes_file_output_location)
    
    
