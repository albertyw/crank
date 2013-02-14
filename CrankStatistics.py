"""
This class receives data from the main Crank class and runs statistics on it

Albert Wang
April 18, 2011
"""

import copy
import os
import time

import Tree

class CrankStatistics:
    """
    This class runs and writes statistics about the raw data from Crank such as 
    score, running time, and HGT counts
    """
    def __init__(self, gene_trees, stat_file_location, true_tree):
        """
        Initialize some variables
        """
        # Raw data from Crank
        self.gene_trees                 = gene_trees
        self.stat_file_location         = stat_file_location
        self.true_tree                  = true_tree
        self.start_time                 = 0
        
        self.times                      = []
        self.base_scores                = []
        self.base_cogboxes              = []
        self.trial_cogboxes             = []
        self.better_trial_operations    = []
        self.memory_usage               = []
    
    ### New Iteration ###
    def new_iteration(self):
        """
        Start a new iteration
        """
        if not os.path.exists(self.stat_file_location):
            os.mkdir(self.stat_file_location)
        self.iteration_time()
        if len(self.base_scores) > 0:
            self.iteration_statistics()
            self.full_statistics()
    
    ### Call Statistics ###
    def iteration_statistics(self):
        """
        Run statistics on the current iteration
        """
        self.better_operations_list(self.stat_file_location+'/better_operations')
        self.leaves_vs_score(self.stat_file_location+'/leaves_vs_score')
        self.leaves_vs_time(self.stat_file_location+'/leaves_vs_time')
        if len(self.base_scores) > 1:
            self.leaves_vs_change_score(self.stat_file_location+'/leaves_vs_change_score')
            
    def full_statistics(self):
        """
        Run statistics on the full run
        """
        self.iteration_vs_time(self.stat_file_location+'/iteration_vs_time')
        self.iteration_vs_score(self.stat_file_location+'/iteration_vs_score')
        self.better_operations_vs_iteration(self.stat_file_location+'/better_operations_vs_iteration')
        self.memory_vs_iteration(self.stat_file_location+'/memory_vs_iteration')
        self.robfo_vs_iteration(self.stat_file_location+"/robfo_vs_iteration")
    
    
    ### Save Statistics ###
    def iteration_time(self):
        """
        Record time to run an iteration
        """
        new_time = time.time()
        if self.start_time != 0:
            iteration_time = int(new_time-self.start_time)
            self.times.append(iteration_time)
        self.start_time = new_time
    
    def add_base_cogbox(self, base_cogbox):
        """
        The cogbox for the base tree
        """
        self.base_cogboxes.append(base_cogbox)
        if len(self.base_cogboxes) > 2:
            self.base_cogboxes[-3] = 0
        
    def add_base_score(self, base_score):
        """
        Receive a base score from Crank
        """
        self.base_scores.append(base_score)
        
    def add_trial_cogboxes(self, trial_cogboxes):
        """
        Receive a list of trial cogboxes that are going to be tested
        """
        self.trial_cogboxes.append(trial_cogboxes)
        if len(self.trial_cogboxes) > 2:
            self.trial_cogboxes[-3] = 0
        
    def add_better_trial_operations(self, better_trial_operations):
        """
        Receive a list of operations that were found to result in better trees
        """
        self.better_trial_operations.append(better_trial_operations)
        print better_trial_operations
        if len(self.better_trial_operations) > 2:
            self.better_trial_operations[-3] = 0
            
    def add_memory_usage(self, memory_usage):
        """
        Receive the memory usage as calculated by the main Crank.py thread
        """
        self.memory_usage.append(memory_usage)
        
        
        
    ### Compute statistics per iteration ###
    def leaves_vs_change_score(self, file_location):
        """
        Compute (leaves in gene tree) vs (change in reconciliation score)
        This should be run per iteration
        """
        current_cogs = self.base_cogboxes[-1].tree_output
        old_cogs = self.base_cogboxes[-2].tree_output
        vs = []
        for current_cog in current_cogs:
            for old_cog in old_cogs:
                if current_cog['name'] == old_cog['name']:
                    tree_name = current_cog['name']
                    gene_tree = self.gene_trees.get_tree_by_name(tree_name)['structure']
                    gene_tree_leaves = Tree.GeneTree(gene_tree).num_leaves()
                    change_score = current_cog['score'] - old_cog['score']
                    vs.append((gene_tree_leaves, change_score))
        
        # Save to file
        current_iteration = len(self.base_cogboxes)
        file_handle = open(file_location+str(current_iteration), 'w')
        file_handle.write(str(vs))
        file_handle.close()
        
    def leaves_vs_score(self, file_location):
        """
        Compute (leaves in gene tree) vs (reconciliation score)
        This should be run per iteration
        """
        current_iteration = len(self.base_cogboxes)
        cogs = self.base_cogboxes[-1].tree_output
        vs = []
        for cog in cogs:
            tree_name = cog['name']
            gene_tree = self.gene_trees.get_tree_by_name(tree_name)['structure']
            gene_tree_leaves = Tree.GeneTree(gene_tree).num_leaves()
            vs.append((gene_tree_leaves, cog['score']))
        
        # Save to file
        file_handle = open(file_location+str(current_iteration), 'w')
        file_handle.write(str(vs))
        file_handle.close()
        
    def leaves_vs_time(self, file_location):
        """
        Compute (leaves in gene tree) vs (time to reconcile gene tree against base tree)
        This should be run per iteration
        """
        current_iteration = len(self.base_cogboxes)
        cogs = self.base_cogboxes[-1].tree_output
        vs = []
        for cog in cogs:
            tree_name = cog['name']
            gene_tree = self.gene_trees.get_tree_by_name(tree_name)['structure']
            gene_tree_leaves = Tree.GeneTree(gene_tree).num_leaves()
            vs.append((gene_tree_leaves, cog['run_time']))
        
        # Save to file
        file_handle = open(file_location+str(current_iteration), 'w')
        file_handle.write(str(vs))
        file_handle.close()
        
            
    def better_operations_list(self, file_location):
        """
        Print a list of better operations
        This should be run per iteration
        """
        current_iteration = len(self.base_cogboxes)
        # Find list padding
        padding0 = 0
        padding1 = 0
        padding2 = 0
        for operation in self.better_trial_operations[-1]:
            padding0 = max(len(str(operation[0])), padding0)
            padding1 = max(len(operation[1][0]), padding1)
            padding2 = max(len(operation[1][1]), padding2)
        
        # Make list
        operation_string = ''
        for operation in self.better_trial_operations[-1]:
            operation_string += str(operation[0]) + ' '*(padding0-len(str(operation[0])))+', '
            operation_string += operation[1][0] + ' '*(padding1-len(operation[1][0]))+', '
            operation_string += operation[1][1] + ' '*(padding2-len(operation[1][1]))+', '
            operation_string += operation[1][2]+"\n"
        
        # Save to file
        file_handle = open(file_location+str(current_iteration), 'w')
        file_handle.write(str(operation_string))
        file_handle.close()
        
    
    ### Compute statistics over the total run ###
    def iteration_vs_time(self, file_location):
        """
        Compute the time it takes per iteration
        This should be run over the total run
        """
        file_handle = open(file_location,'a')
        file_handle.write(str(self.times[-1])+',')
        file_handle.close()
        
    def iteration_vs_score(self, file_location):
        """
        Compute the score per iteration
        This should be run over the total run
        """
        file_handle = open(file_location,'a')
        file_handle.write(str(self.base_scores[-1])+',')
        file_handle.close()
        
    def better_operations_vs_iteration(self, file_location):
        """
        Compute (better_nnis, better_sprs, better_operations) vs (iteration number)
        This should be run over the total run
        """
        better_nnis = 0
        better_sprs = 0
        better_reroots = 0
        for score, operation in self.better_trial_operations[-1]:
            if operation[0] == 'nni':
                better_nnis += 1
            if operation[0] == 'spr':
                better_sprs += 1
            if operation[0] == 'reroot':
                better_reroots += 1
        file_handle = open(file_location,'a')
        file_handle.write(str((better_nnis, better_sprs, better_reroots))+',')
        file_handle.close()
        
        
    def memory_vs_iteration(self, file_location):
        """
        Compute (memory usage) vs (iteration_number)
        This should be run over the total run
        """
        file_handle = open(file_location, 'a')
        file_handle.write(str(self.memory_usage[-1])+',')
        file_handle.close()
        
    def robfo_vs_iteration(self, file_location):
        """
        Compute (robfo score) vs (iteration_number)
        The robfo score is computed between the self.true_tree and self.base_cogbox
        This should be run over the total run
        """
