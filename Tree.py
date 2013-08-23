"""
This Manages Operations On A Tree
This file contains three classes: Tree, SpeciesTree, GeneTree

Albert Wang
December 27, 2010
"""
import copy
import csv
import random
import re
import os
import sys

sys.path.append('./ete')
sys.path.append(os.path.dirname(__file__)+'/ete')
from etetree import Tree as EteTree
sys.path.append('./utilities')
sys.path.append(os.path.dirname(__file__)+'/utilities')
from ReconcileSingle import reconcile_single


class Tree(object):
    """
    General Tree class, this allows for basic tree manipulations
    This is an immutable class
    """
    def __init__(self, tree_structure):
        if tree_structure[-1] != ';':
            tree_structure += ';'
        self.tree_structure = tree_structure
        self.ete = EteTree(tree_structure)

    def __repr__(self):
        return self.ete.write(format=5)

    def num_leaves(self):
        """
        Returns the number of leaves on the tree as an int
        """
        return len(self.ete)

    ### Tree Comparisons ###
    def __eq__(self, other_tree):
        return self.equals(other_tree)

    def equals(self, other_tree):
        """
        Returns whether the tree is the same as another tree with a boolean
        Both trees must be the same type (Tree, SpeciesTree, GeneTree) and
        structure, though not necessarily the same string representation.
        """
        if type(self) != type(other_tree):
            return False
        if self.is_rooted() != other_tree.is_rooted():
            return False
        nodes = [set(node.get_leaf_names()) for node in self.ete.get_descendants()]
        other_tree_nodes = [set(node.get_leaf_names()) for node in other_tree.ete.get_descendants()]
        for node in nodes:
            if node not in other_tree_nodes:
                return False
        return True

    def equals_structure(self, other_tree):
        """
        Like equals() but disregarding branch lengths, only with regards to
        tree structure and leaf names
        """
        return self.standardize_branch_lengths().equals(other_tree.standardize_branch_lengths())

    ### Root/Unroot Functions ###
    def is_rooted(self):
        """ Returns whether the tree is rooted or not as a boolean """
        if len(self.ete.get_children()) == 0:
            return True
        if len(self.ete.get_children()) == 1:
            return len(self.ete.children[0].get_children()) <= 2
        if len(self.ete.get_children()) == 2:
            return True
        if len(self.ete.get_children()) > 2:
            return False

    def get_root(self):
        """
        Get the root node of the Tree
        """
        if self.is_rooted():
            return self.get_leaf_string()
        return None

    def do_root(self, outgroup_leaves):
        """
        Root the tree at the node and return a new Tree instance of it
        outgroup_leaves should be a dash-separated string of all the leaves in the outgroup
        """
        new_tree = copy.deepcopy(self)
        if new_tree.is_rooted():
            new_tree = new_tree.do_unroot()
        if len(new_tree.ete.children) == 1:
            new_tree.ete = new_tree.ete.children[0]
        outgroup = new_tree.find_node(outgroup_leaves)
        if outgroup == None:
            outgroup_leaves = set(new_tree.ete.get_leaf_names()) - set(outgroup_leaves.split('-'))
            outgroup = new_tree.find_node('-'.join(outgroup_leaves))
        new_tree.ete.set_outgroup(outgroup)
        new_tree = new_tree.ete.write(format=5)
        return self.__class__(new_tree)

    def do_unroot(self):
        """
        Unroot the tree and return a new Tree instance of it
        """
        if not self.is_rooted():
            return self
        tree = copy.deepcopy(self.ete)
        if(len(tree.children) == 1):
            tree.children[0].unroot()
        else:
            tree.unroot()
        return Tree(tree.write(format=5))

    ### Node Comparisons ###
    @staticmethod
    def get_node_leaves(node_string):
        """
        This method decomposes the node_string into a list of leaf strings
        """
        leaf_list = node_string.split('-')
        return leaf_list

    def find_node(self, node, exact_match = True):
        """
        This method finds the node from the self.tree that contains the
        node; if exact_match is True, then node must match the
        found node exactly (in any order).  Else, it'll return the closest
        parent node
        """
        node_leaves = Tree.get_node_leaves(node)
        if '>' in self.ete.write(format=5):
            node_leaves = ['>'+leaf for leaf in node_leaves]
        try:
            node_leaves = [self.ete.get_leaves_by_name(leaf)[0] for leaf in node_leaves]
        except IndexError:
            return None
        node = node_leaves[0]
        if(len(node_leaves)>1):
            node = node.get_common_ancestor(*node_leaves)
        if exact_match:
            node_leaves = [leaf.name for leaf in node_leaves]
            if set(node.get_leaf_names()) != set(node_leaves):
                return None
        return node

    def get_node_list(self):
        """
        Get a list of nodes that are in the tree
        """
        return self.ete.get_descendants()

    @staticmethod
    def is_sibling(node1, node2):
        """
        Returns whether node1 and node2 are sibling nodes as a boolean
        """
        return node2 in node1.get_sisters()

    def get_leaf_string(self):
        """
        Get a dash separated string of leaves
        """
        leaves = self.ete.get_leaf_names()
        leaves.sort()
        return '-'.join(leaves)

    def find_ancestor(self, node):
        """
        This method finds all the ancestors of a node on self.tree from the
        node itself to the root.  node is a string and the output is a list
        """
        if type(node) == str:
            node = self.find_node(node)
        ancestors = [node]
        while not node.is_root() and len(node.get_sisters())==1:
            node = node.up
            ancestors.append(copy.deepcopy(node))
        return ancestors

    def find_traversal_length(self, node1, node2):
        """
        This method returns a list of nodes needed to traverse from node1 to
        node2.  The length of the returned list essentially finds how closely
        related node1 and node2 is
        """
        node1 = self.find_node(node1)
        node2 = self.find_node(node2)
        return int(node1.get_distance(node2, topology_only = True))

    def monophyly(self, species, require_all=False):
        """
        This method looks at the tree and returns true if the list of nodes is
        monophyletic (all in one clade, with no missing members)
        nodes should be a list of all species to be considered
        if require_all is True, then this will return False if the species aren't found
        """
        if not require_all:
            species = [specie for specie in species if specie in self.ete.get_leaf_names()]
        if len(species) ==0:
            return True
        if self.find_node('-'.join(species), True) == None:
            return False
        return True


    ### Tree Operations ###
    def standardize_branch_lengths(self):
        """
        Returns a copy of the tree with all branch lengths set to 1
        """
        new_tree = self.tree_structure
        new_tree = re.sub(r':[0-9\.e\-]*',':1.0', new_tree)
        return self.__class__(new_tree)

    def rename_leaves(self, rename_dict = None, csv_file = None):
        """
        Returns a new tree with all leaves renamed based on the csv file or
        rename_dict
        CSV format is:
        find_string, replace_string
        ...
        """
        if rename_dict == None:
            if csv_file == None:
                return copy.deepcopy(self)
            rename_dict = dict({})
            csv_handle = csv.reader(open(csv_file,'rb'))
            for row in csv_handle:
                if row[1] != "":
                    rename_dict[row[0]] = row[1]
        new_tree = copy.deepcopy(self.tree_structure)
        for old_name, new_name in rename_dict.items():
            new_tree = new_tree.replace(old_name+':', new_name+':')
        new_tree = self.__class__(new_tree)
        return new_tree

    def remove_leaves(self, leaves):
        """
        Remove each of the leaves in the argument from the tree and return a new
        tree
        """
        new_tree = copy.deepcopy(self)
        for leaf in leaves:
            if leaf not in new_tree.ete.get_leaf_names():
                continue
            leaves_to_delete = new_tree.ete.get_leaves_by_name(leaf)
            [leaf.delete() for leaf in leaves_to_delete]

        if new_tree.get_node_list() == []:
            new_tree = self.__class__('();')
        else:
            new_tree = self.__class__(str(new_tree))
        return new_tree


    def standardize_leaf_names(self):
        """
        Since PhyML changes leaf names into >Name.GeneNum, this function turns
        leaf names back to normal notation and returns it as the string representation
        of a new tree
        """
        # Remove outer parenthesis around root node and remove branch lengths
        tree = self.standardize_branch_lengths()
        if len(tree.ete.children)==1:
            tree = str(tree)[1:-2]
        else:
            tree = str(tree)
        # Remove '>'
        tree = tree.replace('>','')

        # Remove gene labels from nodes (everything after the period)
        tree = re.sub(r'([(,][A-Za-z0-9]*)\.[0-9]*', r'\1', str(tree))

        # Add a semicolon
        if tree[-1] != ';':
            tree += ';'
        return tree

    def standardize_sister_ordering(self):
        """
        Although a tree is technically the same no matter the order of sister
        nodes as expressed in a newick file, RANGER may consider them different
        trees and give different reconciliation events.  This orders sister
        branches so they are deterministic

        Assumes leaves are unique
        """
        new_tree = copy.copy(self.ete)
        new_tree.sort_descendants()
        new_tree = self.__class__(new_tree.write(format=5))
        return new_tree

    def robinson_foulds(self, other_tree):
        """
        Calculate the Robinson-Foulds score of this tree versus the other tree
        """
        return self.ete.robinson_foulds(other_tree.ete)[0]
    @staticmethod
    def random_tree(leaf_names, rooted=True):
        """
        Create a tree with a random structure with leaves from leaf_names
        """
        tree = EteTree()
        tree.populate(len(leaf_names), leaf_names)
        tree = Tree(tree.write(format=5))
        if not rooted:
            tree = tree.do_unroot()
        return tree


class SpeciesTree(Tree):
    """
    Subclass of Tree, used for operations specific to species trees
    """

    def spr(self, prune, graft):
        """
        SPR the current tree with the supplied prune and graft nodes and
        return the new tree.
        prune and graft are string representations
        """
        new_tree = copy.deepcopy(self)
        prune = new_tree.find_node(prune)
        graft = new_tree.find_node(graft)

        old_parent = prune.up
        old_parent.delete()
        prune.detach()

        ancestor = graft.up
        ancestor.remove_child(graft)
        new_parent = EteTree()
        ancestor.add_child(new_parent)
        graft.detach()
        new_parent.add_child(graft)
        new_parent.add_child(prune)
        return SpeciesTree(new_tree.ete.write(format=5))

    def nni(self, node1, node2):
        """
        Do a Nearest Neighbor Interchange between node1 and node2 and return
        the new tree
        node1 and node2 are string representations
        """

        new_tree = copy.deepcopy(self)
        node1 = new_tree.find_node(node1)
        node2 = new_tree.find_node(node2)

        node1_parent = node1.up
        node2_parent = node2.up

        node1.detach()
        node2.detach()

        node1_parent.add_child(node2)
        node2_parent.add_child(node1)
        return SpeciesTree(new_tree.ete.write(format=5))

    def possible_sprs(self):
        """
        Find the total possible unique SPRs that can be made with the current
        species tree
        The returned possibilities do NOT include SPRs
        1.  between siblings - no change
        2.  between children/ancestors - impossible
        3.  with the same node - no change
        4.  in reverse (not unique)
        """
        possible_sprs = []
        nodes1 = self.get_node_list()
        nodes2 = copy.copy(nodes1)
        for node1 in nodes1:
            for node2 in nodes2:
                if node1 == node2:
                    continue
                # Cannot SPR between siblings
                if node1 in node2.get_sisters():
                    continue
                # Can't SPR with ancestor
                if node2 in node1.get_descendants() or \
                    node1 in node2.get_descendants():
                    continue
                # Can't SPR in parallel
                parallel_spr = False
                for node1_old, node2_old in possible_sprs:
                    if node1 in node1_old.get_sisters() and \
                       node2 in node2_old.get_sisters() and \
                       node1.up == node2.up.up or node2.up == node1.up.up:
                        parallel_spr = True
                        break
                if parallel_spr:
                    continue
                possible_sprs.append((node1, node2))
        possible_sprs = [('-'.join(node1.get_leaf_names()), '-'.join(node2.get_leaf_names())) for (node1, node2) in possible_sprs]
        return possible_sprs

    def possible_nnis(self):
        """
        Find the number of possible unique NNIs that can be made with the current
        species tree
        The returned possibilities do NOT include nnis
        1.  between siblings - no change
        2.  between children/ancestors - impossible
        3.  with the same node - no change
        4.  in reverse (same as another nni)
        5.  in parallel with other nnis (since it would result in the same tree)
        """
        possible_nnis = []
        nodes1 = self.get_node_list()
        nodes2 = copy.copy(nodes1)
        for node1 in nodes1:
            nodes2.remove(node1)
            for node2 in nodes2:
                # Cannot NNI between siblings
                if node1 in node2.get_sisters():
                    continue
                # Can't NNI with ancestor
                if node2 in node1.get_descendants() or \
                    node1 in node2.get_descendants():
                    continue
                # Can't NNI in parallel
                parallel_nni = False
                for node1_old, node2_old in possible_nnis:
                    if node1 in node1_old.get_sisters() and \
                       node2 in node2_old.get_sisters() and \
                       node1.up.up == node2.up.up:
                        parallel_nni = True
                        break
                if parallel_nni:
                    continue
                possible_nnis.append((node1, node2))
        possible_nnis = [('-'.join(node1.get_leaf_names()), '-'.join(node2.get_leaf_names())) for (node1, node2) in possible_nnis]
        return possible_nnis



class GeneTree(Tree):
    """
    Subclass of Tree, used for operations specific to gene trees
    """
    def spr(self, prune, graft):
        """
        Raise a NotImplemented Error because, although it is possible to spr
        this tree, there is no reason to do an spr on a gene tree
        """
        raise NotImplementedError("Why are you trying to SPR a Gene Tree?")

    def unique_leaves(self):
        """
        Return a set of strings of unique leaves (the set of species) covered
        by the gene tree
        """
        leaves = self.ete.get_leaf_names()
        leaves = [leaf[:leaf.find('.')] for leaf in leaves]
        leaves = set(leaves)
        return leaves

    def calculate_weight(self):
        """
        Calculate a weight for the gene tree that is directly proportional to the
        span of the tree (# of unique species) and indirectly proportional to the
        number of repeats
        """

        #species_tree = "((((((((Aerpe:1.0,Hypbu:1.0):1.0,Ignho:1.0):1.0,(Deska:1.0,Stama:1.0):1.0):1.0,(Metse:1.0,(((((Sul04:1.0,Sul27:1.0):1.0,SuliM:1.0):1.0,((Sul14:1.0,Sul51:1.0):1.0,SuliL:1.0):1.0):1.0,Sulso:1.0):1.0,(Sulac:1.0,Sulto:1.0):1.0):1.0):1.0):1.0,((Calma:1.0,(((Pyrae:1.0,Pyrar:1.0):1.0,(Pyris:1.0,Thene:1.0):1.0):1.0,Pyrca:1.0):1.0):1.0,Thepe:1.0):1.0):1.0,((Censy:1.0,Nitma:1.0):1.0,Korcr:1.0):1.0):1.0,Naneq:1.0):1.0,((((Arcfu:1.0,(((((Halla:1.0,Halwa:1.0):1.0,(Halsa:1.0,Halsp:1.0):1.0):1.0,(((Halma:1.0,Halmu:1.0):1.0,Halut:1.0):1.0,Natph:1.0):1.0):1.0,((((Matpa:1.0,Metbo:1.0):1.0,Metcu:1.0):1.0,Methu:1.0):1.0,Metla:1.0):1.0):1.0,(((((Metac:1.0,Metma:1.0):1.0,Metba:1.0):1.0,Metbu:1.0):1.0,Uncme:1.0):1.0,Metsa:1.0):1.0):1.0):1.0,(Picto:1.0,(Theac:1.0,Thevo:1.0):1.0):1.0):1.0,(((((((MetC6:1.0,MetC7:1.0):1.0,(MetmC:1.0,Metmp:1.0):1.0):1.0,Metva:1.0):1.0,Metae:1.0):1.0,((Metfe:1.0,Metja:1.0):1.0,Metvu:1.0):1.0):1.0,((Metsm:1.0,Metth:1.0):1.0,Metst:1.0):1.0):2.0,Metka:1.0):1.0):0.5,(((Pyrab:1.0,Pyrho:1.0):1.0,Pyrfu:1.0):1.0,(((Thega:1.0,Theko:1.0):1.0,Theon:1.0):1.0,Thesi:1.0):1.0):1.0):0.5):1.0"
        #cog = reconcile_single(species_tree, self)
        #numhgts = str(cog.events).count('hgt')
        #weight = numhgts #numhgts\
        #brn_node = cog.events[0][7:]
        #brn_leaves = set(brn_node.split('-'))
        #weight = len(brn_leaves) #brnleaves
        #weight = len(self.ete.get_leaf_names()) #numleaves
        #weight = len(set(self.ete.get_leaf_names())) # uniqueleaves
        weight = 1
        return weight
        """
        # Weight = (unique species) / avg(number of repeats per species)
        leaves = [leaf[:leaf.find('.')] for leaf in self.ete.get_leaf_names()]
        repeats = 1
        for leaf in set(leaves):
            repeats += leaves.count(leaf)-1
        weight = 1.0 * len(set(leaves)) / (repeats)
        return weight

        # Weight = (unique species) / sum((number of leaves)/(1 species))
        leaves = [leaf[:leaf.find('.')] for leaf in self.ete.get_leaf_names()]
        repeats = 1
        for leaf in set(leaves):
            repeats += leaves.count(leaf)-1
        weight = 1.0 * len(leaves) / repeats
        return weight
        """

if __name__ == "__main__":
    import doctest
    doctest.testmod()
