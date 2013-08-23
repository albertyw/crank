"""
This program, when given a list of leaves to keep, will remove all other leaves 
from a species tree and GenesFile.  This helps with reducing complexity of 
reconciliations and therefore runtime.  


"""
import sys
sys.path.append('/home/albertyw/crank/src/')
import Tree
import GenesFile

if len(sys.argv) < 3:
    print 'Argument 1: species tree input ("-" for no tree)'
    print 'Argument 2: species tree output ("-" for no tree)'
    print 'Argument 3: genesfile input (blank for no genesfile)'
    print 'Argument 4: genesfile output (blank for no genesfile)'
species_tree_input = sys.argv[1]
species_tree_output = sys.argv[2]
strip_genesfile = False
if len(sys.argv) > 3:
    strip_genesfile = True
    genesfile_input = sys.argv[3]
    genesfile_output = sys.argv[4]

strip_species_tree = True
if species_tree_input == '-':
    strip_species_tree = False
    

# The list of leaf names to keep
all_leaves = set(['Natph', 'Pyris', 'Halwa', 'Halsp', 'Pyrca', 'Methu', \
        'Metsa', 'MetC6', 'MetC7', 'Picto', 'Halla', 'Metja', 'Halut', 'Halsa', \
        'Calma', 'Ignho', 'Metva', 'Censy', 'SuliL', 'Metst', 'Metae', 'Hypbu', \
        'SuliM', 'Pyrfu', 'Sul27', 'Nitma', 'Metsm', 'Metbu', 'Sulto', 'Thevo', \
        'Metfe', 'Sul51', 'Theon', 'Korcr', 'Metba', 'Thene', 'Deska', 'Metac', \
        'Metmp', 'Metbo', 'Theko', 'Thesi', 'Sul04', 'Metth', 'Halma', 'Sulac', \
        'Theac', 'Metvu', 'Arcfu', 'Metka', 'Metma', 'Halmu', 'Sul14', 'Metse', \
        'Uncme', 'Thega', 'Matpa', 'Thepe', 'Pyrab', 'Sulso', 'Naneq', 'Pyrae', \
        'Metcu', 'Aerpe', 'Pyrho', 'MetmC', 'Pyrar', 'Metla', 'Stama'])
keep_leaves = set(['Naneq', 'Thesi', 'Pyrfu', 'Metka', 'Metst', 'Metth', \
        'Metvu', 'MetC6', 'Picto', 'Thevo', 'Metsa', 'Metac', 'Metla', 'Matpa', \
        'Natph', 'Halla', 'Arcfu', 'Nitma', 'Censy', 'Korcr', 'Thepe', 'Calma', \
        'Sul04', 'Metse', 'Ignho', 'Aerpe'])
remove_leaves = all_leaves - keep_leaves

if strip_species_tree:
    # Read the original species tree
    a = open(species_tree_input,'r')
    species = a.read()
    a.close()
    tree = Tree.SpeciesTree(species)
    
    # Modify the species tree
    tree = tree.remove_leaves(remove_leaves)
    
    # Save the species tree
    a = open(species_tree_output, 'w')
    a.write(str(tree))
    a.close()

if strip_genesfile:
    # Read the original genesfile
    genes_file = GenesFile.GenesFile(genesfile_input)
    
    # Modify the genesfile
    tree_id = 0
    while tree_id < len(genes_file.trees):
        print tree_id
        tree = genes_file.trees[tree_id]
        tree_object = Tree.GeneTree(Tree.GeneTree(tree['structure']).standardize_leaf_names())
        tree_object = tree_object.remove_leaves(remove_leaves)
        if tree_object.num_leaves() <= 4:
            genes_file.tree.pop(tree_id)
            continue
        tree['structure'] = str(tree_object)
        tree['weight'] = tree_object.calculate_weight()
        #tree['boots'] = [boot.remove_leaves(remove_leaves) for boot in tree['boots']]
        tree['boots'] = []
        genes_file.trees[tree_id] = tree
        
        tree_id += 1
    
    # Save the genesfile
    genes_file.write_file(genesfile_output)


