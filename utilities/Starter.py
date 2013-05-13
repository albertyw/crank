import os
import random
import sys
crank_path = "/home/albertyw/crank/"
sys.path.append(crank_path)
import Crank
import Tree

# Static Options
penalty_dict = dict({'hgt':3,'dup':2,'los':1,'spc':0})
spr_search_width = 100
nni_search_width = 'all'
max_iterations = 3
job_queue = 'speedy'
erase_previous_run = True
correct_tree_structure = None
use_darwin = False
use_albertyw = False
use_mitmunc = False

num_trials = 50
test_path = "/home/albertyw/tester/changer_small_full/"
gene_trees_file_location = test_path + "/GenesFile"
brochier_tree_file_location = test_path + "brochier.tree"
brochier_tree_file_handle = open(brochier_tree_file_location,'r')
brochier_tree_structure = brochier_tree_file_handle.read().strip()
brochier_tree_file_handle.close()
for trial_num in range(num_trials):
    brochier_tree = Tree.SpeciesTree(brochier_tree_structure)
    choose_random = True
    nodes = brochier_tree.get_node_list()
    while choose_random:
        # Select two random nodes
        select1 = random.randint(0, len(nodes)-1)
        select2 = random.randint(0, len(nodes)-1)
        node1 = nodes[select1]
        node2 = nodes[select2]
        if node1 in node2.get_sisters():
            continue                        # Siblings or Same node
        if node1.get_leaf_names() in [ancestor.get_leaf_names() for ancestor in brochier_tree.find_ancestor(node2)] or \
           node2.get_leaf_names() in [ancestor.get_leaf_names() for ancestor in brochier_tree.find_ancestor(node1)]:
            continue                        # Can't nni with ancestor
        choose_random = False
    node1 = '-'.join(node1.get_leaf_names())
    node2 = '-'.join(node2.get_leaf_names())
    # Create mutated tree
    if random.randint(0,1) == 0:
        # SPR
        change = 'spr'
        test_tree = brochier_tree.spr(node1, node2)
    else:
        # NNI
        change = 'nni'
        test_tree = brochier_tree.nni(node1, node2)
    
    # Save tree
    species_tree_file_location = test_path + str(trial_num)+ "/test_species.tree"
    species_tree_structure = str(test_tree)
    if not os.path.exists(test_path + str(trial_num)):
        os.mkdir(test_path + str(trial_num))
    species_tree_handle = open(species_tree_file_location,'w')
    species_tree_handle.write(species_tree_structure)
    species_tree_handle.close()
    output_directory = test_path + str(trial_num)+ "/output/"
    
    # Save change log
    change_file = open(test_path + str(trial_num)+"/change",'w')
    change_file.write(change+"\n"+node1+"\n"+node2)
    change_file.close()
    
    print "Species Tree File:",species_tree_file_location
    print "Gene Tree File:",gene_trees_file_location
    print "Output Directory",output_directory
    print change
    print "From:   ", node1
    print "Parent: ", '-'.join(brochier_tree.find_node(node1).up.get_leaf_names())
    print "To:     ", node2
    print "Parent: ", '-'.join(brochier_tree.find_node(node2).up.get_leaf_names())
    
    
    starter = Crank.Crank(species_tree_structure,\
                    gene_trees_file_location,\
                    penalty_dict,\
                    output_directory,\
                    spr_search_width,\
                    nni_search_width,\
                    max_iterations,\
                    job_queue,\
                    erase_previous_run,\
                    correct_tree_structure,\
                    use_darwin,\
                    use_albertyw,\
                    use_mitmunc
                   )
    print 'running'
    starter.run()
    print 'end'
    print
    print
