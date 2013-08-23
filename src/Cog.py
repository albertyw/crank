"""
Manages A Cog (single species tree, single gene tree)
This also manages direct interaction with AnGST

Albert Wang
Updated January 2012 for DTL
"""
import os
import re
import subprocess
import sys
import tempfile
import Tree

parent_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append('./ete')
sys.path.append(os.path.dirname(__file__)+'/ete')
from etetree import Tree as EteTree


class Cog:
    """
    This class interacts with AnGST to run a single reconciliation
    """
    def __init__(self, species_tree, genes_file_tree, penalties):
        """
        species_tree should be the species tree string in newick format
        genes_file_tree should be a dictionary, like one of the entries from GenesFile
        penalties is a dictionary of penalties to be used during reconcilation
        All three variables should be immutable
        Also create some default reconciliation variables
        """
        self.DTL_LOCATION = parent_path+'/include/dtl'
        self.species_tree = species_tree
        self.name = genes_file_tree['name']
        self.weight = genes_file_tree['weight']
        self.boots = genes_file_tree['boots']
        self.gene_tree_structure = genes_file_tree['structure']
        self.penalties = penalties
        # Default Reconciliation Variables
        self.run = False
        self.score = -1      # AnGST Score
        self.run_time = -1   # seconds
        self.hgts = []       # List of HGTs reported by AnGST
        self.events = []     # List of All events reported by AnGST


    def reconcile(self):
        """
        Run the reconciliation.
        The reconciliation results will be piped directly into this class
        """
        command, input_file_location = self.__create_input_obj()
        output_args = self.__run_angst(command)
        self.__parse_output_args(output_args, input_file_location)
        os.unlink(input_file_location)


    def __create_input_obj(self):
        """
        Create the correct inputs
        """
        # Root the gene tree for dtl
        gene_tree = EteTree(self.gene_tree_structure)
        if len(gene_tree.get_children()) > 2:
            gene_tree.set_outgroup(gene_tree.get_leaves()[0])
        gene_tree = gene_tree.write(format=5)


        species_tree = self.species_tree.standardize_leaf_names()
        gene_tree = Tree.GeneTree(gene_tree)
        gene_tree = gene_tree.standardize_leaf_names()

        # Create the input file
        input_file, input_file_location = tempfile.mkstemp(text=True)
        input_file = os.fdopen(input_file, "w")
        input_file_text = species_tree + "\n[&U]" + gene_tree
        input_file.write(input_file_text)
        input_file.close()

        # Create command to run dtl
        command = self.DTL_LOCATION+' '
        command += '-i '+str(input_file_location)+' '
        command += '-D '+str(self.penalties['dup'])+' '
        command += '-T '+str(self.penalties['hgt'])+' '
        command += '-L '+str(self.penalties['los'])+' '
        command += '--seed 1 '
        #command += '--type 2'
        return command, input_file_location

    def __run_angst(self, command):
        """
        Actually run AnGST and grab its output
        """
        # Spawn dtl subprocess
        output = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = output.stdout.read()
        stderr = output.stderr.read()

        if stderr!='':
            print stderr

        return stdout

    def __parse_output_args(self, output, input_file_location):
        """
        Parse the outputted values of DTL
        """
        self.run = True
        output = output.split("\n")
        if "Species Tree: " not in output:
            print 'ERROR'
            print input_file_location
            print "\n".join(output)
        output = output[output.index("Species Tree: "):]

        brn = False
        recordEvents = False
        events = []
        for line in output:
            # Find reconciliation events
            if line == '':
                recordEvents = False
            if recordEvents == True:
                events.append(line)
            if line == 'Reconciliation:':
                recordEvents = True

            # Find brn node
            if brn == True:
                line = EteTree(line)
                brn = self.get_leaves(line)
            if line == 'Optimally rooted Gene Tree: ':
                brn = True

            # Find score and number of losses
            if 'The minimum reconciliation cost' in line:
                self.score = int(line[36:line.find(' ',36)])
                num_losses = int(line[line.rfind(' ')+1:-1])


        # Get nodes on species tree
        nodes = {}
        species_tree = output[1]
        species_tree = EteTree(species_tree, format=8)
        for node in species_tree.traverse():
            name = node.name
            nodes[name] = self.get_leaves(node)

        # Read Events
        #events.reverse()
        for index, event in enumerate(events):
            # CUR
            if 'Leaf Node' in event:
                events[index] = '[cur]: '+event[0:event.find(':')]
                brn = event[0:event.find(':')]
            # SPC
            if 'Speciation' in event:
                nodeId = event[event.rfind(' ')+1:]
                events[index] = '[spc]: ' + nodes[nodeId]
                brn = nodes[nodeId]
            # HGT
            if 'Transfer' in event:
                donor = re.search(r'Mapping --> ([a-zA-Z0-9\.]*)\,', event).group(1)
                recipient = re.search(r'Recipient --> ([a-zA-Z0-9\.]*)$', event).group(1)
                donor = nodes[donor]
                recipient = nodes[recipient]
                events[index] = '[hgt]: ' + donor + ' --> '+recipient
                self.hgts.append('[hgt]: ' + donor + ' --> '+recipient)
                brn = donor
            # LOS
            # Doesn't actually contain loss events

            # DUP
            if 'Duplication' in event:
                nodeId = event[event.rfind(' ')+1:]
                events[index] = '[dup]: ' + nodes[nodeId]
                brn = nodes[nodeId]
        events.reverse()

        events += ['[los]']*num_losses
        self.events = ['[brn]: '+brn] + events
        self.weighted_score = Cog.compute_hgt_weighted_score(self.events, self.species_tree, self.penalties, self.weight)

    @staticmethod
    def compute_hgt_weighted_score(angst_events, species_tree, penalty_dict, weight, hgt_weight = 1.0):
        """
        This method reads the list of events of a cog and calculates the
        distance with the hgt penalty based on the distance of the hgt
        """
        weighted_score = 0
        i = 0
        while i < len(angst_events):
            event = Cog.parse_event(angst_events[i])
            if event[0] == 'cur' or event[0] == 'brn':
                i += 1
                continue
            if event[0] == 'hgt':
                nodes_traversed = species_tree.find_traversal_length(event[1], event[2])
                hgt_modifier = hgt_weight*nodes_traversed / species_tree.num_leaves()
                weighted_score += penalty_dict['hgt'] + hgt_modifier
            else:
                weighted_score += penalty_dict[event[0]]
            i += 1
        weighted_score *= weight
        return weighted_score

    @staticmethod
    def parse_event(event_string):
        """
        This method reads a single event's AnGST string representation and
        returns a tuple of the node.  e.g. ('hgt', '3','5')
        """
        # Find event type
        event_type = event_string[1:4]
        if event_type == 'hgt': # Look for two nodes
            node_string1 = event_string[7:event_string.find('-->')-1]
            node_string2 = event_string[event_string.find('-->')+4:]
            parsed_event = (event_type, node_string1, node_string2)
        else:                   # Look for only one node
            node_string = event_string[7:]
            parsed_event = (event_type, node_string)
        return parsed_event

    """
    Turn an ete tree into a dash separated leaves
    """
    def get_leaves(self, node):
        node = node.write(format=9)
        node = re.sub(r'^[(]+','', node)
        node = re.sub(r'[);]+$','', node)
        return re.sub(r'[(),]+','-', node)

class InputObj:
    """ Class for the passing of variables into AnGST """
    def __init__(self):
        """  Initialize default values """
        self.species_tree = None
        self.ultra_tree_bool = False
        self.boots = None
        self.output_dir = "/home/albertyw/angst_test/"
        self.penalties_filename = None
        self.hgt_penalty = 3
        self.dup_penalty = 2
        self.los_penalty = 1
        self.spc_penalty = 0
        self.special = None
        self.outgroup = None
        self.luca = None
        self.hr_scaling = 0.0
        self.iterate = None
        self.penalty_weight = 0.0
        self.event_guide_fn = None

if __name__ == "__main__":
    print "doctest"
    import doctest
    doctest.testmod()
