"""
This program takes two outputs of the base tree output and compares differences
in scores of the same gene trees
A third file is the csv list of cog names and their human-readable names
The fourth file contains the GenesFile
"""

import sys
import csv

sys.path.append('/home/albertyw/crank/src/')
import Tree
import GenesFile
import CogBox
import Cog

class Gene_Tree_Compare:
    def __init__(self, output_file_1, species_tree_1, output_file_2, species_tree_2, cog_descriptions_file, genes_file):
        self.file_1 = output_file_1
        #species_tree_1_handle = open(species_tree_1,'r')
        #species_tree_1 = species_tree_1_handle.read()
        #species_tree_1_handle.close()
        #self.cogbox_1 = CogBox.CogBox(Tree.SpeciesTree(species_tree_1), '','',dict({'hgt':3,'dup':2,'los':1,'spc':0}),'')
        self.file_2 = output_file_2
        #species_tree_2_handle = open(species_tree_2,'r')
        #species_tree_2 = species_tree_2_handle.read()
        #species_tree_2_handle.close()
        #self.cogbox_2 = CogBox.CogBox(Tree.SpeciesTree(species_tree_2), '','',dict({'hgt':3,'dup':2,'los':1,'spc':0}),'')
        self.cog_descriptions_file = cog_descriptions_file
        self.genes_file = genes_file

    def compare(self):
        file_1 = csv.reader(open(self.file_1, 'rb'), delimiter=',')
        file_2 = csv.reader(open(self.file_2, 'rb'), delimiter=',')
        cog_descriptions_file = csv.reader(open(self.cog_descriptions_file, 'rb'), delimiter="\t")
        genes_file = GenesFile.GenesFile(self.genes_file)

        output_1 = dict({})
        for row in file_1:
            output_1[row[0]] = [row[2], row[3], row[5].count('hgt'), self.find_species_brn(row[5])]
            #output_1[row[0]] = [row[2], 0, row[4].count('hgt'), self.find_species_brn(row[4])]
        output_2 = dict({})
        for row in file_2:
            output_2[row[0]] = [row[2], row[3], row[5].count('hgt'), self.find_species_brn(row[5])]
            #output_2[row[0]] = [row[2], 0, row[4].count('hgt'), self.find_species_brn(row[4])]
        cog_descriptions = dict({})
        for row in cog_descriptions_file:
            cog_descriptions[row[0]] = row[2]


        score_differences = []
        for cog_name, info in output_1.iteritems():
            row = dict({})
            row['cog_name'] = cog_name
            row['cog_description'] = cog_descriptions[cog_name]

            row['score_1'], row['score_1_weighted'], row['num_hgt_1'], row['species_brn_1'] = info
            row['score_2'], row['score_2_weighted'], row['num_hgt_2'], row['species_brn_2'] = output_2[cog_name]
            if cog_name not in output_2.keys():
                continue
            row['score_difference'] = float(row['score_1']) - float(row['score_2'])
            row['score_difference_weighted'] = float(row['score_1_weighted']) - float(row['score_2_weighted'])

            tree = genes_file.get_tree_by_name(cog_name)
            row['tree_leaves'] = tree['tree'].num_leaves()
            row['unique_leaves'] = len(tree['tree'].unique_leaves())

            score_differences.append(row)

        score_differences = sorted(score_differences, key=lambda difference: difference['score_difference_weighted'])
        return score_differences

    def find_species_brn(self, event):
        return event[:event.find('\'',2)].count('-')+1

    def print_output(self, score_differences):
        print 'cog_name, score_1, score_2, score_difference, score_1_weighted, score_2_weighted, score_difference_weighted, cog_description, tree_leaves, unique_leaves, num_hgt_1, num_hgt_2, species_brn_1, species_brn_2'
        for row in score_differences:
            print row['cog_name'],'|',\
                row['score_1'],'|',\
                row['score_2'],'|',\
                row['score_difference'],'|',\
                row['score_1_weighted'],'|',\
                row['score_2_weighted'],'|',\
                row['score_difference_weighted'],'|',\
                row['cog_description'],'|',\
                row['tree_leaves'],'|',\
                row['unique_leaves'],'|',\
                row['num_hgt_1'],'|',\
                row['num_hgt_2'],'|',\
                row['species_brn_1'],'|',\
                row['species_brn_2'],'|'

