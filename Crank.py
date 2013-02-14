"""
The Main Execution Thread of Crank

Albert Wang
January 14, 2011
"""

import copy
import os
import random
import shutil
import time

from CrankStatistics import CrankStatistics
from Cog import Cog
from CogBox import CogBox
from GenesFile import GenesFile
from Tree import SpeciesTree
from Scheduler import Scheduler

import PyVM

class Crank:
    """
    The top level class that is called from outside
    """
    def __init__(self, \
                 species_tree_structure,\
                 gene_trees_file_location,\
                 penalty_dict,\
                 output_directory,\
                 spr_search_width,\
                 nni_search_width,\
                 max_iterations,\
                 job_queue,\
                 erase_previous_run = True,\
                 correct_tree_structure = None,\
                 use_darwin  = True,\
                 use_albertyw = True,\
                 use_mitmunc = True,\
                 species_trees_per_job = 2,\
                ):
        """
        Initialize Variables then check if there is already previous run data
        species_tree_structure - the structure of the species tree
        gene_trees_file_location - the location of the Gene Trees File
        penalty_dict - A dictionary of AnGST penalties
        output_directory - The directory to output all data to
        spr_search_width - The max number of sprs to try per iteration
        nni_search_width - The max number of nnis to try per iteration
        max_iterations - The maximum number of iterations to run Crank
        erase_previous_run - Whether to erase data from previous runs
        correct_tree_structure - The structure of the correct tree to compare to
        """
        self.gene_trees           = GenesFile(gene_trees_file_location)
        self.species_tree         = SpeciesTree(species_tree_structure)
        self.penalty_dict         = penalty_dict
        self.output_directory     = output_directory
        self.spr_search_width     = spr_search_width
        self.nni_search_width     = nni_search_width
        self.iteration_number     = 1
        self.max_iterations       = max_iterations
        self.max_operations_per_iteration = 2
        self.reverse_spr          = True
        self.species_tree_history = [str(self.species_tree)]
        self.log_file_location    = self.output_directory+"/output.txt"
        self.shell_file_directory = self.output_directory +"/shell/"
        self.scheduler            = Scheduler(job_queue, \
                                              self.shell_file_directory,\
                                              use_darwin,\
                                              use_albertyw,\
                                              use_mitmunc,\
                                              gene_trees_file_location,\
                                              species_trees_per_job)
        if correct_tree_structure == None:
            self.true_tree        = None
        else:
            self.true_tree        = SpeciesTree(correct_tree_structure)
        self.statistics           = CrankStatistics(self.gene_trees, \
            self.output_directory+"/stats", self.true_tree)
        self.memtest_location = self.output_directory+"/meminfo.txt"
        self.__load_run_data(erase_previous_run)
        
    def run_iteration(self):
        """
        Run one iteration of Crank
        """
        
        self.write_log_file("ITERATION "+str(self.iteration_number))
        # Create iteration folder
        iteration_folder = self.output_directory+"/"+str(self.iteration_number)
        os.mkdir(iteration_folder)
        base_tree_file_location = iteration_folder+"/base.tree"
        base_tree_file_handle = open(base_tree_file_location,'w')
        base_tree_file_handle.write(str(self.species_tree))
        base_tree_file_handle.close()
        
        # Reconcile base tree
        base_cogbox = self.reconcile_base_tree(iteration_folder)
        self.statistics.add_base_cogbox(base_cogbox)
        # We should now have a finished full reconciliation of the base tree
        # The data for the reconciliation is stored at base_reconciliation_output
        
        # Evaluate base tree
        base_score = self.evaluate_base_tree(base_cogbox)
        self.statistics.add_base_score(base_score)
        self.write_log_file("")
        
        # Choose SPRs
        spr_trial_trees = self.choose_sprs(base_cogbox)
        # We now have a list of parsed sprs in spr_list
        
        # Choose NNIs
        nni_trial_trees = self.choose_nnis(base_cogbox)
        
        # Choose Reroots
        reroot_trial_trees = self.choose_reroots(base_cogbox)
        
        # Create trial trees
        trial_trees = spr_trial_trees + nni_trial_trees + reroot_trial_trees
        del spr_trial_trees
        del nni_trial_trees
        del reroot_trial_trees
        # We now have a list of trial trees to test with
        
        # Reconcile trial trees
        trial_cogboxes = self.reconcile_trial_trees(trial_trees, iteration_folder)
        del trial_trees
        self.statistics.add_trial_cogboxes(trial_cogboxes)
        
        # Evaluate trial trees
        better_trial_operations = self.evaluate_trial_trees(trial_cogboxes, base_score)
        del trial_cogboxes
        self.statistics.add_better_trial_operations(better_trial_operations)
        
        # Create new base tree
        finished = self.create_new_base_tree(better_trial_operations)
        del better_trial_operations
        
        if finished == True:
            return False
            
        self.write_log_file("")
        self.write_log_file("")
        self.iteration_number += 1
        return True
        
    def reconcile_base_tree(self, iteration_folder):
        """
        Reconcile the base tree with every gene tree
        """
        # Create base tree folder
        base_tree_folder = iteration_folder+"/base/"
        os.mkdir(base_tree_folder)
        
        # Create and submit the cogbox
        base_tree = copy.deepcopy(self.species_tree)
        selected_trees = self.gene_trees.get_trees()
        base_cogbox = CogBox(base_tree, \
            self.gene_trees, \
            selected_trees, \
            self.penalty_dict, \
            self.scheduler)
        info_file_location = base_tree_folder+"input"
        output_file_location = base_tree_folder+"output"
        base_cogbox.run(info_file_location, output_file_location)
        
        # Run the job and wait until finished
        real_reconciliation_time = time.time()
        self.scheduler.run_job()
        self.scheduler.wait_until_finish()
        real_reconciliation_time = time.time() - real_reconciliation_time
        base_cogbox.statistics['real_run_time'] = real_reconciliation_time
        base_cogbox.read_output()
        
        return base_cogbox
        
    def evaluate_base_tree(self, base_cogbox):
        """
        Read the output and run some statistics on the base cogbox
        """
        # Calculate statistics
        self.write_log_file("Base Tree Weighted Score: "+\
            str(base_cogbox.statistics['average_hgt_weighted_score']))
        #str(base_cogbox.statistics['average_score']))
        self.write_log_file("Base Tree Unique HGT: "+\
            str(len(base_cogbox.statistics['hgt_frequencies'])))
        self.write_log_file("Base Tree Unique Events: "+\
            str(len(base_cogbox.statistics['event_frequencies'])))
        self.write_log_file("Base Tree Real Time: "+\
            str(base_cogbox.statistics['real_run_time']))
        self.write_log_file("Base Tree CPU Time: "+\
            str(base_cogbox.statistics['cpu_run_time']))
        #return base_cogbox.statistics['average_score']
        return base_cogbox.statistics['average_hgt_weighted_score']
        
        
    def choose_sprs(self, base_cogbox):
        """
        This method parses the output of the base tree reconciliations
        It will then choose the best SPRs to run
        """
        # Sort sprs by frequency
        hgt_frequencies = base_cogbox.statistics['hgt_frequencies']
        hgt_frequencies_list = hgt_frequencies.items()
        hgt_frequencies_list = sorted(hgt_frequencies_list, key=lambda hgt: hgt[1])
        hgt_frequencies_list.reverse()
        
        # Skim off top self.spr_search_width
        spr_search_width = self.spr_search_width
        if spr_search_width == 'all' or spr_search_width > len(hgt_frequencies_list):
            spr_search_width = len(hgt_frequencies_list)
        trial_trees = [0] * spr_search_width
        if self.reverse_spr:
            trial_trees *= 2
        i = 0
        while i < spr_search_width:
            hgt = Cog.parse_event(hgt_frequencies_list[i][0])[1:]
            spr = ('spr', hgt[1], hgt[0])
            new_tree = self.species_tree.spr(spr[1], spr[2])
            trial_trees[i] = (new_tree, spr)
            if self.reverse_spr:
                spr = ('spr', hgt[0], hgt[1])
                new_tree = self.species_tree.spr(spr[1], spr[2])
                trial_trees[i + spr_search_width] = (new_tree, spr)
            i += 1
        return trial_trees
        
    
    def choose_nnis(self, base_cogbox):
        """
        Choose nodes to run nearest neighbor interchange on.  
        Currently, this only chooses random nodes
        """
        # Skim off top self.nni_search_width of nnis
        trial_trees = []
        all_nnis = self.species_tree.possible_nnis()
        random.shuffle(all_nnis)
        nni_search_width = self.nni_search_width
        if nni_search_width == 'all' or nni_search_width > len(all_nnis):
            nni_search_width = len(all_nnis)
        
        i = 0
        while i < nni_search_width:
            node1, node2 = all_nnis[i]
            new_tree = self.species_tree.nni(node1, node2)
            trial_trees.append((new_tree, ('nni', node1, node2)))
            i += 1
        return trial_trees
        
    def choose_reroots(self, base_cogbox):
        """
        Choose outgroups to reroot to
        Only move the root to an adjacent node
        """
        # Find the children of the current tree
        root = self.species_tree.ete
        if len(root.children)==1:
            root = root.children[0]
        child1, child2 = root.children
        # Find outgroups and make trees
        trial_trees = []
        if not child1.is_leaf():
            outgroup = child1.children[0]
            root = self.species_tree.do_root('-'.join(outgroup.get_leaf_names()))
            change = ('reroot', '-'.join(root.get_leaf_string()), '-'.join(outgroup.get_leaf_names()))
            trial_trees.append((root, change))
        if not child2.is_leaf():
            outgroup = child2.children[0]
            root = self.species_tree.do_root('-'.join(outgroup.get_leaf_names()))
            change = ('reroot', root.get_leaf_string(), '-'.join(outgroup.get_leaf_names()))
            trial_trees.append((root, change))
        return trial_trees
        
        
    def reconcile_trial_trees(self, trial_trees, iteration_dir, selected_tree_cutoff=0):
        """
        Reconcile the trial trees
        """
        # Create trial tree folder
        trial_tree_dir = iteration_dir+"/trial/"
        os.mkdir(trial_tree_dir)
        trial_info = open(iteration_dir+"/trial_info",'w')
        
        # Create and submit the cogboxes
        trial_cogboxes = [0]*len(trial_trees)
        i = 0
        cutoff = 0 ################### CHANGE THIS ############################
        while i < len(trial_trees):
            trial_tree, trial_operation = trial_trees[i]
            selected_trees = self.gene_trees.get_trees(cutoff)
            trial_cogbox = CogBox(trial_tree, \
                self.gene_trees, \
                selected_trees, \
                self.penalty_dict, \
                self.scheduler)
            trial_cogbox.trial_operation = trial_operation
            trial_info.write(str(i)+','+str(trial_operation)+"\n")
            info_file_location = trial_tree_dir+str(i)+"input"
            output_file_location = trial_tree_dir+str(i)+"output"
            trial_cogbox.run(info_file_location, output_file_location)
            trial_cogboxes[i] = trial_cogbox
            i += 1
        
        # Run the job and wait until finished
        trial_info.close()
        real_reconciliation_time = time.time()
        self.scheduler.run_job()
        self.scheduler.wait_until_finish()
        real_reconciliation_time = time.time() - real_reconciliation_time
        trial_cogboxes[0].statistics['real_run_time'] = real_reconciliation_time
        
        return trial_cogboxes
        
    
    def evaluate_trial_trees(self, trial_cogboxes, base_score):
        """
        Find which trials resulted in trees that are better or equal to the base tree
        Example Output:
        [(5, ('spr', '5', '7')), (4, ('nni', '10', '15'))]
        """
        # Calculate run time statistics
        
        cpu_reconciliation_time = 0
        for trial_cogbox in trial_cogboxes:
            trial_cogbox.read_output()
            cpu_reconciliation_time += trial_cogbox.statistics['cpu_run_time']
        self.write_log_file("Trial Trees Real Time: "+\
            str(trial_cogboxes[0].statistics['real_run_time']))
        self.write_log_file("Trial Trees CPU Time: "+\
            str(cpu_reconciliation_time))
        
        # Find better cogboxes
        better_trial_operations = []
        sprs_tried = 0
        nnis_tried = 0
        reroots_tried = 0
        sprs_better = 0
        nnis_better = 0
        reroots_better = 0
        for trial_cogbox in trial_cogboxes:
            trial_operation = trial_cogbox.trial_operation
            trial_score = trial_cogbox.statistics['average_hgt_weighted_score']
            if trial_operation[0] == 'spr':
                sprs_tried += 1
            if trial_operation[0] == 'nni':
                nnis_tried += 1
            if trial_operation[0] == 'reroot':
                reroots_tried += 1
            if trial_score < base_score:
                if trial_operation[0] == 'spr':
                    sprs_better += 1
                if trial_operation[0] == 'nni':
                    nnis_better += 1
                if trial_operation[0] == 'reroot':
                    reroots_better += 1
                better_trial_operations.append((trial_score, trial_operation))
        
        trial_cogboxes = []
        
        # Output information about statistics
        self.write_log_file("Trial Trees Better SPRs: "+str(sprs_better)+'/'+str(sprs_tried))
        self.write_log_file("Trial Trees Better NNIs: "+str(nnis_better)+'/'+str(nnis_tried))
        self.write_log_file("Trial Trees Better Reroots: "+str(reroots_better)+'/'+str(reroots_tried))
        better_trial_operations = sorted(better_trial_operations, key=lambda op: op[0])
        return better_trial_operations
        
    def create_new_base_tree(self, better_trial_operations):
        """
        Given a list of better trial operations, apply them to the base tree
        There is a limit to the number of operations that can be completed
        """
        operations_done = 1
        touched_leaves = set([])
        if len(better_trial_operations) == 0:
            return True
        for score, operation in better_trial_operations:
            operation_type = operation[0]
            node1 = operation[1]
            node2 = operation[2]
            if operations_done >= self.max_operations_per_iteration:
                break
            
            # Check that there aren't any conflicts
            cancel = False
            leaves = set(node1.split('-') + node2.split('-'))
            for leaf in leaves:
                if leaf in touched_leaves:
                    cancel = True
                    break
            if cancel:
                continue
            
            # Create a new tree
            if operation_type == 'spr':
                self.species_tree = self.species_tree.spr(node1, node2)
            elif operation_type == 'nni':
                self.species_tree = self.species_tree.nni(node1, node2)
            elif operation_type == 'reroot':
                self.species_tree = self.species_tree.do_root(node2)
                
            touched_leaves = touched_leaves.union(leaves)
            self.write_log_file("Changes Completed: "+str(score)+" - "+str(operation))
            operations_done += 1
        self.species_tree = self.species_tree.standardize_branch_lengths()
        return False
    
    def run(self):
        """
        The main method for the running of Crank
        This method just runs run_iteration() a lot of times
        There should be code to actually stop running sometime
        """
        self.write_log_file("Started Crank")
        self.statistics.new_iteration()
        # Iterate while there are untaken paths
        while self.iteration_number < self.max_iterations:
            
            continue_iterations = self.run_iteration()
            self.statistics.add_memory_usage(PyVM.TotalMemory())
            self.statistics.new_iteration()
            if not continue_iterations:
                self.write_log_file("Tree has converged")
                break
        self.write_log_file("Ended Crank After "+str(self.iteration_number)+' Iterations')
        
    def __load_run_data(self, erase_previous_run):
        """
        Look in self.output_directory and check if this is a continuation of 
        an old run.  If it is, then load the old run data.  If it isn't then 
        don't do anything
        This function doesn't do much checking to make sure that the data is 
        correct
        """
        # Setup Output Directory
        if erase_previous_run and os.path.exists(self.output_directory):
            shutil.rmtree(self.output_directory)
        if not os.path.exists(self.output_directory):
            os.mkdir(self.output_directory)
        if os.path.exists(self.shell_file_directory):
            shutil.rmtree(self.shell_file_directory)
        os.mkdir(self.shell_file_directory)
        os.mkdir(self.shell_file_directory+'/finished')
        os.chmod(self.shell_file_directory+'/finished', 0777)
        
        # See if there's data in the output directory
        while True:
            iteration_path = self.output_directory+'/'+\
                str(self.iteration_number)
            if not os.path.exists(iteration_path):
                self.iteration_number -=1
                iteration_path = self.output_directory+'/'+\
                    str(self.iteration_number)
                break
            self.iteration_number += 1
        
        # Load the old data
        if self.iteration_number > 0:
            old_species_tree_location = iteration_path+'/base.tree'
            old_species_tree_handle = open(old_species_tree_location,'r')
            old_species_tree = old_species_tree_handle.read()
            old_species_tree_handle.close()
            self.species_tree = SpeciesTree(old_species_tree)
            self.write_log_file("Found Old Species Tree at "+\
                old_species_tree_location)
            self.write_log_file("Starting Species Tree: "+\
                str(self.species_tree))
            
            shutil.rmtree(iteration_path)
        else:
            self.iteration_number = 1
        
    def write_log_file(self, text):
        """
        Write messages to a human-readable log file
        """
        text = time.strftime("%Y-%m-%d %H:%M:%S  ")+text
        print text
        log_file = open(self.log_file_location,'a')
        log_file.write(text+"\n")
        log_file.close()

    def write_memtest(self, text):
        """
        Write messages for testing memory usage
        """
        text = str(text)+" - " + str(PyVM.TotalMemory())+" MB"
        print text
        log_file = open(self.memtest_location,'a')
        log_file.write(text+"\n")
        log_file.close()
