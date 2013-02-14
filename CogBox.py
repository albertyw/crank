"""
Manages Operations on a Cog Box (Single species tree, all gene trees)
This class does not interact with Cog.py.  Instead it only uses the output of 
Cog.py

Albert Wang
February 19, 2011
"""

import csv

from Cog import Cog

class CogBox:
    """
    This class handles the logic behind single species tree, all gene tree 
    reconciliations.  This does stuff such as summary statistics, scoring, etc. 
    This also writes the input data for runs and reads the output, though the 
    runs are done with Cog through Scheduler
    """
    def __init__(self, species_tree, gene_trees, selected_trees, \
        penalty_dict, scheduler):
        """
        Initialize some basic variables
        species_tree is an instance of SpeciesTree in Tree.py
        gene_trees is an instance of GenesFile in GenesFile.py
        selected_trees is a list of tree names to be loaded
        scheduler is the global instance of Scheduler from Scheduler.py
        trial_operation is used by Crank.py to keep track of how the Cogbox tree was created
        output_file_location is the file location to write the run output
        tree_output is the raw statistics read from output_file_location
        statistics is the computed statistics on the job
        
        """
        self.species_tree = species_tree
        self.gene_trees = gene_trees
        self.selected_trees = selected_trees
        self.penalty_dict = penalty_dict
        self.scheduler = scheduler
        self.trial_operation = ()
        self.output_file_location = ""
        self.tree_output = []
        self.statistics = dict({})
        
    def run(self, info_file_location, output_file_location):
        """
        This loads the runs into the scheduler
        """
        self.output_file_location = output_file_location
        # Create the info file for Job
        info_file_handle = open(info_file_location, 'w')
        info_file_handle.write(str(self.species_tree)+"\n")
        info_file_handle.write(self.gene_trees.file_location+"\n")
        info_file_handle.write(str(self.selected_trees)+"\n")
        info_file_handle.write(str(self.penalty_dict)+"\n")
        info_file_handle.write(self.output_file_location+"\n")
        info_file_handle.close()
        # Submit to scheduler
        self.scheduler.submit_job(info_file_location)
        
    def read_output(self):
        """
        This function will read the file at output_file_location and update 
        self.tree_output with raw data and will call self.calculate_statistics()
        which will calculate statistics on the raw data
        """
        output_file_handle = csv.reader(open(self.output_file_location, 'rb'), \
            delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for line in output_file_handle:
            cog = dict({})
            cog['name'] = line[0]
            cog['weight'] = float(line[1])
            cog['score'] = float(line[2])
            cog['weighted_score'] = float(line[3])
            cog['run_time'] = float(line[4])
            cog['events'] = eval(line[5])
            self.tree_output.append(cog)
        self.calculate_statistics()
    
    def calculate_statistics(self):
        """
        Calculate statistics 
        """
        # Total Run Time
        total_run_time = sum([cog['run_time'] for cog in self.tree_output])
        self.statistics['cpu_run_time'] = total_run_time
        
        # Average Score
        weighted_scores = [cog['score'] * cog['weight'] for cog in self.tree_output]
        average_score = sum(weighted_scores)/len(self.tree_output)
        self.statistics['average_score'] = average_score
        
        # Average HGT-Distance Weighted Score
        weighted_scores = [cog['weighted_score'] for cog in self.tree_output]
        average_score = sum(weighted_scores)/len(self.tree_output)
        self.statistics['average_hgt_weighted_score'] = average_score
        
        # Average Unweighted Score
        unweighted_scores = [cog['score'] for cog in self.tree_output]
        average_score = sum(unweighted_scores)/len(self.tree_output)
        self.statistics['average_unweighted_score'] = average_score
        
        # Median Score
        unweighted_scores.sort()
        average_score = unweighted_scores[len(unweighted_scores)/2]
        self.statistics['median_score'] = average_score
        
        # Events
        events = [event for cog in self.tree_output for event in cog['events']]
        self.statistics['events'] = events
        
        # Event/HGT  Frequencies
        event_frequencies = dict({})
        hgt_frequencies = dict({})
        for event in events:
            if event in event_frequencies:
                event_frequencies[event] += 1
            else:
                event_frequencies[event] = 1
            if event[1:4] == 'hgt':
                if event in hgt_frequencies:
                    hgt_frequencies[event] += 1
                else:
                    hgt_frequencies[event] = 1
        self.statistics['event_frequencies'] = event_frequencies
        self.statistics['hgt_frequencies'] = hgt_frequencies
    

    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
