"""
This program takes two trees as arguments and compares them to each other
"""


import os
import sys
sys.path.append('/home/albertyw/crank/src/')

import Tree

tree1_location = sys.argv[1]
tree2_location = sys.argv[2]

tree1_handle = open(tree1_location,'r')
tree1 = tree1_handle.read()
tree1 = Tree.Tree(tree1)
tree1_handle.close()

tree2_handle = open(tree2_location,'r')
tree2 = tree2_handle.read()
tree2 = Tree.Tree(tree2)
tree2_handle.close()

print "Tree String Equals:", str(tree1) == str(tree2)
print "Tree Equals:", tree1.equals(tree2)
print "Tree Structure Equals:", tree1.equals_structure(tree2)
print
print "Tree1 Rooted:", tree1.is_rooted()
print "Tree2 Rooted:", tree2.is_rooted()
