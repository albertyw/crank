import sys

crank_path = "/home/albertyw/crank/"
test_path = "/home/albertyw/tester/artificial_tests/mukul2/random_species_1/no_weight/"
sys.path.append(crank_path)
import Crank

species_tree_file_location = "/home/albertyw/tester/rawdata/mukul2/species_trees/rand1.tree"
species_tree_file_handle = open(species_tree_file_location,'r')
species_tree_structure = species_tree_file_handle.read().strip()
species_tree_file_handle.close()
gene_trees_file_location = "/home/albertyw/tester/rawdata/mukul2/genes_files/no_weight_simulated"
penalty_dict = dict({'hgt':3,'dup':2,'los':1,'spc':0})
output_directory = test_path + "output/"
spr_search_width = 100
nni_search_width = 100
max_iterations = 50
job_queue = 'short'
erase_previous_run = False
correct_tree_structure = None
use_darwin = False
use_albertyw = False
use_mitmunc = False

print "Species Tree File:",species_tree_file_location
print "Gene Tree File:",gene_trees_file_location
print "Output Directory",output_directory

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
