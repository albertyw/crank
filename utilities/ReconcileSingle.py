"""
This file takes a species tree and a gene tree, reconciles them on the current 
node/machine, and returns a cog with the reconciliation output.  

This is a shortcut for reconciling stuff
"""
import os
import sys
sys.path.append('/home/albertyw/crank/src/')

import Cog
import Tree

def reconcile_single(species_tree, gene_tree, penalties = {'dup': 2, 'los': 1, 'hgt': 3, 'spc': 0}):
    if type(species_tree) == str:
        species_tree = Tree.SpeciesTree(species_tree)
    if type(gene_tree) == str:
        gene_tree = Tree.GeneTree(gene_tree)
        
        
    gene_tree = dict({'structure':str(gene_tree)})
    gene_tree['name'] = ''
    gene_tree['weight'] = 1
    gene_tree['boots'] = []
    cog = Cog.Cog(species_tree, gene_tree, penalties)
    cog.reconcile()
    
    # cog.name
    # cog.weight
    # cog.score
    # cog.weighted_score
    # cog.run_time
    # cog.events
    return cog



