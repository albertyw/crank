"""
This program reads the trees from a GenesFile and compares how many species each
set of gene trees shares, then writes the output to an html file
"""

import sys

sys.path.append('/home/albertyw/crank/src/')
import GenesFile
import Tree

#a = Tree.GeneTree("(((((((>MetC7.150402949:0.035279,(>Metmp.45357591:0.041409,>MetC6.159905306:0.040339):0.013600):0.013847,>MetmC.134046679:0.050693):0.139306,>Metva.150399773:0.213660):0.121400,>Metae.150401566:0.235223):0.042061,((>Metja.15668308:0.072055,>Metfe.256810324:0.084821):0.094265,>Metvu.261402423:0.196506):0.258147):0.651434,>Metst.84489002:0.604863):0.115310,>Metth.15679494:0.548854,>Metsm.148643314:0.465090);")
#print a.num_leaves()
#leaves = []
#print a.tree.leaf_dict

def find_leaves(tree):
    tree_name = tree['name']
    tree = tree['tree']
    leaves = tree.tree.leaf_dict.keys()
    leaves = set([leaf[:leaf.find('.')] for leaf in leaves])
    return tree_name, leaves

def find_overlapping_leaves(leaves_a, leaves_b):
    return len(leaves_a.intersection(leaves_b))


gene_location = '/home/albertyw/leaf_overlap/GenesFile'
gene_location = sys.argv[1]
a = GenesFile.GenesFile(gene_location)
matrix = dict({})
tree_names = []
for tree in a.trees:
    tree_a_name, tree_a_leaves = find_leaves(tree)
    matrix[tree_a_name] = dict({})
    tree_names.append(tree_a_name)
    for tree in a.trees:
        tree_b_name, tree_b_leaves = find_leaves(tree)
        matrix[tree_a_name][tree_b_name] = find_overlapping_leaves(tree_a_leaves, tree_b_leaves)


print '<table>'
print '<tr><th></th>'
for name in tree_names:
    print '<th>'+name+'</th>'
print '</tr>'
for name_a in tree_names:
    print '<tr><th>'+name_a+'</th>'
    for name_b in tree_names:
        print '<td>'+str(matrix[name_a][name_b])+'</td>'
    print '</tr>'
print '</table>'


