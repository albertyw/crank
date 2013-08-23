"""
This program reads gene trees and computes the number of overlapping gene trees
for every set of species.
"""


import csv, sys

sys.path.append('/home/albertyw/crank/src/')
import GenesFile
import Tree

#a = Tree.GeneTree("(((((((>MetC7.150402949:0.035279,(>Metmp.45357591:0.041409,>MetC6.159905306:0.040339):0.013600):0.013847,>MetmC.134046679:0.050693):0.139306,>Metva.150399773:0.213660):0.121400,>Metae.150401566:0.235223):0.042061,((>Metja.15668308:0.072055,>Metfe.256810324:0.084821):0.094265,>Metvu.261402423:0.196506):0.258147):0.651434,>Metst.84489002:0.604863):0.115310,>Metth.15679494:0.548854,>Metsm.148643314:0.465090);")
#print a.num_leaves()
#leaves = []
#print a.tree.leaf_dict

def find_leaves(tree):
    tree = tree['tree']
    leaves = tree.tree.leaf_dict.keys()
    leaves = set([leaf[:leaf.find('.')] for leaf in leaves])
    return leaves

def add_new_species(matrix, species):
    matrix[species] = dict({})
    for leaf in matrix.keys():
        matrix[leaf][species] = 0
        matrix[species][leaf] = 0
    return matrix


def num_to_hex(number):
    number = int(round(number))
    if number < 10:
        return str(number)+str(number)
    elif number == 10:
        return 'AA'
    elif number == 11:
        return 'BB'
    elif number == 12:
        return 'CC'
    elif number == 13:
        return 'DD'
    elif number == 14:
        return 'EE'
    else:
        return 'FF'

def calculate_color(number, largest_num, smallest_num):
    percentage = 1.0*(number-smallest_num)/(largest_num-smallest_num)
    if percentage >.5:
        green = 16
        if percentage-0.5 == 0:
            red = 0
        else:
            red = (1.0-percentage)*2*16
    else:
        red = 16
        if percentage == 0:
            green = 0
        else:
            green = percentage*2*16
    color = num_to_hex(red)+num_to_hex(green)+'00'
    return color

def find_max_min_num(matrix):
    largest_num = 0
    smallest_num = 99999999999
    for a in matrix.keys():
        for b in matrix[a].keys():
            if largest_num < matrix[a][b]:
                largest_num = matrix[a][b]
            if smallest_num > matrix[a][b]:
                smallest_num = matrix[a][b]
    return largest_num, smallest_num


gene_location = sys.argv[1]
a = GenesFile.GenesFile(gene_location)
matrix = dict({})
species_names = []
for tree in a.trees:
    leaves = find_leaves(tree)
    for leaf in leaves:
        if leaf not in species_names:
            species_names.append(leaf)
            matrix = add_new_species(matrix, leaf)
    for leaf in leaves:
        for leaf_b in leaves:
            matrix[leaf][leaf_b] += 1


largest_num, smallest_num = find_max_min_num(matrix)
print '<b>Largest Overlap:</b>'+str(largest_num)
print '<br />'
print '<b>Smallest Overlap:</b>'+str(smallest_num)
print '<table>'
print '<tr><th></th>'
for species in species_names:
    print '<th>'+species+'</th>'
print '<th>Total Gene trees with species</th>'
print '</tr>'
for species_a in species_names:
    print '<tr><th>'+species_a+'</th>'
    for species_b in species_names:
        color = calculate_color(matrix[species_a][species_b], largest_num, smallest_num)
        print '<td><font color="'+color+'">'+str(matrix[species_a][species_b])+'</font></td>'
    print '<td><font color="'+color+'">'+str(matrix[species_a][species_a])+'</font></td>'
    print '</tr>'
print '<tr>'
print '<th>Total Gene trees with species</th>'
for species_a in species_names:
    print '<td><font color="'+color+'">'+str(matrix[species_a][species_a])+'</font></td>'
print '</tr>'
print '</table>'

