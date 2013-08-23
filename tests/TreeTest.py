import copy
import os
import sys
import unittest

sys.path.append('../')
sys.path.append(os.path.dirname(__file__)+'/../')
import Tree

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        # Main Tree
        self.treeA = Tree.Tree("(((1.6:1.6,(10.7:10.7,5.8:5.8):1):2,6.1:6.1):3);")
        # Large Tree
        self.treeB = Tree.Tree("((10:0.0153845,(3:0.011536,((((4:0.087852,9:0.110919):0.021808,(6:0.104141,1:0.104029):0.017502):0.016738,(8:0.058348,(7:0.034947,2:0.043808):0.023238):0.068127):0.09458,5:0.028769):0.030769):0.0153845):0.01);")
        # Same as treeA but expressed differently
        self.treeC = Tree.Tree("((6.1:6.1,(1.6:1.6,(10.7:10.7,5.8:5.8):1):2):3);")
        # Structurally same as treeA but with standardized branch lengths
        self.treeD = Tree.Tree("(((1.6:1,(10.7:1,5.8:1):1):1,6.1:1):1);")
        # Unrooted version of treeA
        self.treeE = Tree.Tree('((1.6:1.6,(10.7:10.7,5.8:5.8):1.0,6.1:6.1):3);')
        
        
        # Copies for Species Tree
        # Main Tree
        self.speciesTreeA = Tree.SpeciesTree("(((1.6:1.6,(10.7:10.7,5.8:5.8):1):2,6.1:6.1):3);")
        # Large Tree
        self.speciesTreeB = Tree.SpeciesTree("((10:0.0153845,(3:0.011536,((((4:0.087852,9:0.110919):0.021808,(6:0.104141,1:0.104029):0.017502):0.016738,(8:0.058348,(7:0.034947,2:0.043808):0.023238):0.068127):0.09458,5:0.028769):0.030769):0.0153845):0.01);")
        # Same as treeA but expressed differently
        self.speciesTreeC = Tree.SpeciesTree("((6.1:6.1,(1.6:1.6,(10.7:10.7,5.8:5.8):1):2):3);")
        # Structurally same as treeA but with standardized branch lengths
        self.speciesTreeD = Tree.SpeciesTree("(((1.6:1,(10.7:1,5.8:1):1):1,6.1:1):1);")
        # Unrooted version of treeA
        self.speciesTreeE = Tree.SpeciesTree('((1.6:1.6,(10.7:10.7,5.8:5.8):1.0,6.1:6.1):3);')
        
    def tearDown(self):
        # Main Tree
        treeA = Tree.Tree("(((1.6:1.6,(10.7:10.7,5.8:5.8):1):2,6.1:6.1):3);")
        self.assertEqual(self.treeA, treeA)
        # Large Tree
        treeB = Tree.Tree("((10:0.0153845,(3:0.011536,((((4:0.087852,9:0.110919):0.021808,(6:0.104141,1:0.104029):0.017502):0.016738,(8:0.058348,(7:0.034947,2:0.043808):0.023238):0.068127):0.09458,5:0.028769):0.030769):0.0153845):0.01);")
        self.assertEqual(self.treeB, treeB)
        # Same as treeA but expressed differently
        treeC = Tree.Tree("((6.1:6.1,(1.6:1.6,(10.7:10.7,5.8:5.8):1):2):3);")
        self.assertEqual(self.treeC, treeC)
        # Structurally same as treeA but with standardized branch lengths
        treeD = Tree.Tree("(((1.6:1,(10.7:1,5.8:1):1):1,6.1:1):1);")
        self.assertEqual(self.treeD, treeD)
        # Unrooted version of treeA
        treeE = Tree.Tree('((1.6:1.6,(10.7:10.7,5.8:5.8):1.0,6.1:6.1):3);')
        self.assertEqual(self.treeE, treeE)
        
        # Copies for Species Tree
        # Main Tree
        speciesTreeA = Tree.SpeciesTree("(((1.6:1.6,(10.7:10.7,5.8:5.8):1):2,6.1:6.1):3);")
        self.assertEqual(self.speciesTreeA, speciesTreeA)
        # Large Tree
        speciesTreeB = Tree.SpeciesTree("((10:0.0153845,(3:0.011536,((((4:0.087852,9:0.110919):0.021808,(6:0.104141,1:0.104029):0.017502):0.016738,(8:0.058348,(7:0.034947,2:0.043808):0.023238):0.068127):0.09458,5:0.028769):0.030769):0.0153845):0.01);")
        self.assertEqual(self.speciesTreeB, speciesTreeB)
        # Same as speciesTreeA but expressed differently
        speciesTreeC = Tree.SpeciesTree("((6.1:6.1,(1.6:1.6,(10.7:10.7,5.8:5.8):1):2):3);")
        self.assertEqual(self.speciesTreeC, speciesTreeC)
        # Structurally same as speciesTreeA but with standardized branch lengths
        speciesTreeD = Tree.SpeciesTree("(((1.6:1,(10.7:1,5.8:1):1):1,6.1:1):1);")
        self.assertEqual(self.speciesTreeD, speciesTreeD)
        # Unrooted version of speciesTreeA
        speciesTreeE = Tree.SpeciesTree('((1.6:1.6,(10.7:10.7,5.8:5.8):1.0,6.1:6.1):3);')
        self.assertEqual(self.speciesTreeE, speciesTreeE)
        
    def test_init(self):
        self.assertEqual(str(self.treeA), '(((1.6:1.6,(10.7:10.7,5.8:5.8):1):2,6.1:6.1):3);')
        self.assertEqual(str(self.treeB), "((10:0.0153845,(3:0.011536,((((4:0.087852,9:0.110919):0.021808,(6:0.104141,1:0.104029):0.017502):0.016738,(8:0.058348,(7:0.034947,2:0.043808):0.023238):0.068127):0.09458,5:0.028769):0.030769):0.0153845):0.01);")
        
    def test_leaves(self):
        self.assertEqual(self.treeA.num_leaves(), 4)
        self.assertEqual(self.treeB.num_leaves(), 10)
        
    def test_equals(self):
        self.assertTrue(self.treeA.equals(copy.deepcopy(self.treeA)))
        self.assertTrue(self.treeA.equals(self.treeC))
        self.assertFalse(self.treeA.equals(self.treeB))
        self.assertTrue(self.treeA.equals(Tree.Tree('(((1.6:1.6,(10.7:10.7,5.8:5.8):1):2,6.1:6.1):3);')))
        self.assertTrue(self.treeA.equals(Tree.Tree('(((1.6:1.600,(10.7:10.7,5.8:5.8):1):2,6.1:6.1):3);')))
        self.assertEqual(self.treeA, Tree.Tree('(((1.6:1.600,(10.7:10.7,5.8:5.8):1):2,6.1:6.1):3);'))
            
    def test_equals_structure(self):
        self.assertTrue(self.treeA.equals(copy.deepcopy(self.treeA)))
        self.assertTrue(self.treeA.equals(self.treeC))
        self.assertFalse(self.treeA.equals(self.treeB))
        self.assertTrue(self.treeD.equals(self.treeA))
        self.assertFalse(self.treeD.equals(self.treeB))
        self.assertTrue(self.treeD.equals(self.treeC))
        
        self.assertTrue(self.speciesTreeA.equals(copy.deepcopy(self.speciesTreeA)))
        self.assertTrue(self.speciesTreeA.equals(self.speciesTreeC))
        self.assertFalse(self.speciesTreeA.equals(self.speciesTreeB))
        self.assertTrue(self.speciesTreeD.equals(self.speciesTreeA))
        self.assertFalse(self.speciesTreeD.equals(self.speciesTreeB))
        self.assertTrue(self.speciesTreeD.equals(self.speciesTreeC))
            
    def test_is_rooted(self):
        self.assertFalse(self.treeE.is_rooted())
        self.assertTrue(self.treeA.is_rooted())
        
    def test_get_root(self):
        self.assertEquals(self.treeA.get_root(), '1.6-10.7-5.8-6.1')
        self.assertEquals(self.treeE.get_root(), None)
    
    def test_do_root(self):
        self.assertTrue(self.treeE.do_root('10.7-5.8-1.6').equals_structure(self.treeA))
        self.assertTrue(self.treeE.do_root('6.1').equals_structure(self.treeA))
        self.assertTrue(self.treeA.do_root('10.7-5.8-1.6').equals_structure(self.treeA))
        
    def test_do_unroot(self):
        self.assertTrue(self.treeA.do_unroot().equals_structure(self.treeE))
        self.assertTrue(self.treeC.do_unroot().equals_structure(self.treeE))
        self.assertTrue(self.treeD.do_unroot().equals_structure(self.treeE))
        self.assertTrue(self.treeE.do_unroot().equals_structure(self.treeE))
        
    def test_get_node_leaves(self):
        self.assertEqual(Tree.Tree.get_node_leaves("1.6"), ['1.6'])
        self.assertEqual(Tree.Tree.get_node_leaves("1.6-10.7-5.8"), ['1.6', '10.7', '5.8'])
        
    def test_find_node(self):
        self.assertEqual(str(self.treeA.find_node("1.6")), "\n--1.6")
        self.assertEqual(self.treeA.find_node("10.7-1.6"), None)
        self.assertEqual(str(self.treeA.find_node("10.7-1.6", False)), "\n   /-1.6\n--|\n  |   /-10.7\n   \\-|\n      \\-5.8")
        
    def test_get_node_list(self):
        nodes = self.treeA.get_node_list()
        nodes = ['-'.join(node.get_leaf_names()) for node in nodes] 
        nodes = set(nodes)
        self.assertEquals(nodes, set(['1.6', '10.7-5.8', '10.7', '5.8', '1.6-10.7-5.8', '1.6-10.7-5.8-6.1', '6.1']))
        
        
    def test_is_sibling(self):
        nodes = self.treeA.get_node_list()
        sorted(nodes)
        self.assertFalse(Tree.Tree.is_sibling(nodes[0], nodes[0]))
        self.assertFalse(Tree.Tree.is_sibling(nodes[0], nodes[1]))
        self.assertFalse(Tree.Tree.is_sibling(nodes[0], nodes[2]))
        self.assertFalse(Tree.Tree.is_sibling(nodes[0], nodes[3]))
        self.assertFalse(Tree.Tree.is_sibling(nodes[0], nodes[4]))
        self.assertFalse(Tree.Tree.is_sibling(nodes[0], nodes[5]))
        self.assertFalse(Tree.Tree.is_sibling(nodes[0], nodes[6]))
        self.assertFalse(Tree.Tree.is_sibling(nodes[1], nodes[0]))
        self.assertFalse(Tree.Tree.is_sibling(nodes[1], nodes[1]))
        self.assertTrue(Tree.Tree.is_sibling(nodes[1], nodes[2]))
        self.assertFalse(Tree.Tree.is_sibling(nodes[1], nodes[3]))
        self.assertFalse(Tree.Tree.is_sibling(nodes[1], nodes[4]))
        self.assertFalse(Tree.Tree.is_sibling(nodes[1], nodes[5]))
        self.assertFalse(Tree.Tree.is_sibling(nodes[1], nodes[6]))
        self.assertFalse(Tree.Tree.is_sibling(nodes[3], nodes[0]))
        self.assertFalse(Tree.Tree.is_sibling(nodes[3], nodes[1]))
        self.assertFalse(Tree.Tree.is_sibling(nodes[3], nodes[2]))
        self.assertFalse(Tree.Tree.is_sibling(nodes[3], nodes[3]))
        self.assertTrue(Tree.Tree.is_sibling(nodes[3], nodes[4]))
        self.assertFalse(Tree.Tree.is_sibling(nodes[3], nodes[5]))
        self.assertFalse(Tree.Tree.is_sibling(nodes[3], nodes[6]))
        
    def test_get_leaf_string(self):
        self.assertEquals(self.treeA.get_leaf_string(), '1.6-10.7-5.8-6.1')
        self.assertEquals(self.treeB.get_leaf_string(), '1-10-2-3-4-5-6-7-8-9')
        self.assertEquals(self.treeC.get_leaf_string(), '1.6-10.7-5.8-6.1')
        self.assertEquals(self.treeD.get_leaf_string(), '1.6-10.7-5.8-6.1')
        self.assertEquals(self.treeE.get_leaf_string(), '1.6-10.7-5.8-6.1')
        
    def test_find_ancestor(self):
        ancestors = self.speciesTreeA.find_ancestor("1.6")
        ancestors = [ancestor.get_leaf_names() for ancestor in ancestors]
        self.assertEquals(ancestors, [['1.6'], ['1.6', '10.7', '5.8'], ['1.6', '10.7', '5.8', '6.1']])
        
        ancestors = self.speciesTreeA.find_ancestor("5.8")
        ancestors = [ancestor.get_leaf_names() for ancestor in ancestors]
        self.assertEquals(ancestors, [['5.8'], ['10.7', '5.8'], ['1.6', '10.7', '5.8'], ['1.6', '10.7', '5.8', '6.1']])
        
        
    def test_find_traversal_length(self):
        self.assertEquals(self.treeA.find_traversal_length("1.6", "6.1"), 2)
        self.assertEquals(self.treeA.find_traversal_length("1.6", "1.6"), 0)
        self.assertEquals(self.treeA.find_traversal_length("1.6", "10.7"), 2)
        
    def test_monophyly(self):
        self.assertTrue(self.treeA.monophyly([]))
        self.assertTrue(self.treeA.monophyly(['10.7', '5.8']))
        self.assertTrue(self.treeA.monophyly(['10.7', '5.8', '1.6']))
        self.assertTrue(self.treeA.monophyly(['10.7', '5.8', '2345']))
        self.assertTrue(self.treeE.monophyly(['10.7', '5.8']))
        self.assertTrue(self.treeB.monophyly(['7', '2', '8']))
        self.assertFalse(self.treeA.monophyly(['10.7', '1.6']))
        self.assertFalse(self.treeE.monophyly(['10.7', '5.8', '1.6']))
        self.assertFalse(self.treeB.monophyly(['4', '9', '6']))
        species = ["Halma", "Halsa", "Halsp", "Halmu", "Halwa", "Halut", "Halla", "Natph"]
        asdf = Tree.GeneTree("(Halwa:1.000000,Halma:1.000000,Halmu:1.000000);")
        self.assertTrue(asdf.monophyly(species))
        species = ['Arcfu']
        self.assertTrue(asdf.monophyly(species))
        
    def test_standardize_branch_lengths(self):
        self.assertEquals(self.treeA.standardize_branch_lengths(), self.treeD)
        self.assertEquals(self.treeC.standardize_branch_lengths(), self.treeD)
        self.assertEquals(self.treeD.standardize_branch_lengths(), self.treeD)
        treeA = Tree.Tree("(((1.6:1e-08,(10.7:1e-08,5.8:5.8):1):2,6.1:6.1):3);")
        self.assertNotEquals(self.treeA, self.treeD)
        self.assertEquals(treeA.standardize_branch_lengths(), self.treeD)
        
    def test_rename_leaves(self):
        renamed_tree = Tree.Tree("(((a:1.6,(b:10.7,c:5.8):1):2,d:6.1):3);")
        rename_dict = dict({})
        rename_dict['1.6'] = 'a'
        rename_dict['10.7'] = 'b'
        rename_dict['5.8'] = 'c'
        rename_dict['6.1'] = 'd'
        self.assertEquals(self.treeA.rename_leaves(rename_dict=rename_dict), renamed_tree)
        
    def test_remove_leaves(self):
        treeA_removed = Tree.Tree("((1.6:2,6.1:6.1):3);")
        treeD_removed = Tree.Tree("((1.6:1,6.1:1):1);")
        treeE_removed = Tree.Tree('((1.6:1.6,6.1:6.1):3);')
        leaves = ['10.7', '5.8']
        self.assertEquals(self.treeA.remove_leaves(leaves), treeA_removed)
        self.assertEquals(self.treeC.remove_leaves(leaves), treeA_removed)
        self.assertEquals(self.treeD.remove_leaves(leaves), treeD_removed)
        self.assertEquals(self.treeE.remove_leaves(leaves), treeE_removed)
        treeA_removed = Tree.Tree("(((1.6:1.6,5.8:5.8):2,6.1:6.1):3);")
        leaves = ['10.7']
        self.assertEquals(self.treeA.remove_leaves(leaves), treeA_removed)
        treeA_removed = Tree.Tree("((1.6:1.6,(10.7:10.7,5.8:5.8):1):2);")
        leaves = ['6.1']
        self.assertEquals(self.treeA.remove_leaves(leaves), treeA_removed)
        leaves = ['6.1', '1.6', '10.7', '5.8']
        self.assertEquals(self.treeA.remove_leaves(leaves), Tree.Tree("();"))
        
    def test_standardize_leaf_names(self):
        treeA_standardized = '((1:1,(10:1,5:1):1):1,6:1):1;'
        treeB_standardized = '(10:1,(3:1,((((4:1,9:1):1,(6:1,1:1):1):1,(8:1,(7:1,2:1):1):1):1,5:1):1):1):1;'
        treeC_standardized = '(6:1,(1:1,(10:1,5:1):1):1):1;'
        treeD_standardized = '((1:1,(10:1,5:1):1):1,6:1):1;'
        treeE_standardized = '(1:1,(10:1,5:1):1,6:1):1;'
        
        self.assertEquals(self.treeA.standardize_leaf_names(), treeA_standardized)
        self.assertEquals(self.treeB.standardize_leaf_names(), treeB_standardized)
        self.assertEquals(self.treeC.standardize_leaf_names(), treeC_standardized)
        self.assertEquals(self.treeD.standardize_leaf_names(), treeD_standardized)
        self.assertEquals(self.treeE.standardize_leaf_names(), treeE_standardized)
        
    def test_standardize_sister_ordering(self):
        self.assertEquals(str(self.treeA.standardize_sister_ordering()), str(self.treeA))
        self.assertEquals(str(self.treeC.standardize_sister_ordering()), str(self.treeA))
        treeA_copy = copy.deepcopy(self.treeA.ete)
        treeA_copy.get_descendants()[1].swap_children()
        treeA_copy.get_descendants()[3].swap_children()
        treeA_copy = Tree.Tree(treeA_copy.write(format=5))
        self.assertNotEquals(str(treeA_copy), str(self.treeA))
        self.assertEquals(str(treeA_copy.standardize_sister_ordering()), str(self.treeA))
        
    def test_robinson_foulds(self):
        self.assertEquals(self.treeA.robinson_foulds(self.treeC), 0)
        self.assertEquals(self.treeA.robinson_foulds(self.treeD), 0)
        self.assertEquals(self.treeA.robinson_foulds(self.treeE), 1)
        
    def test_random_tree(self):
        leaves = [str(i) for i in range(1,6)]
        rand_tree = Tree.Tree.random_tree(leaves)
        self.assertEquals(rand_tree.num_leaves(), 5)
        self.assertEquals(Tree.Tree.get_node_leaves(rand_tree.get_leaf_string()), leaves)
        self.assertTrue(rand_tree.is_rooted())
        rand_tree = Tree.Tree.random_tree(leaves, False)
        self.assertEquals(rand_tree.num_leaves(), 5)
        self.assertEquals(Tree.Tree.get_node_leaves(rand_tree.get_leaf_string()), leaves)
        self.assertFalse(rand_tree.is_rooted())
        
    def test_spr(self):
        spr_tree = Tree.SpeciesTree("((((10.7:10.7,1.6:1.6):1,5.8:5.8):2,6.1:6.1):3);")
        prune = "1.6"
        graft = "10.7"
        self.assertTrue(self.speciesTreeA.spr(prune, graft).equals_structure(spr_tree))
        
        spr_tree = Tree.SpeciesTree("((1.6:1,(6.1:6,(10.7:10,5.8:5):1):1):3);")
        prune = "10.7-5.8"
        graft = "6.1"
        self.assertTrue(self.speciesTreeA.spr(prune, graft).equals_structure(spr_tree))
        
        self.assertTrue(self.speciesTreeA.equals(self.speciesTreeC))
    
    def test_nni(self):
        spr_tree = Tree.SpeciesTree("((((5.8:1,1.6:1):1,10.7:1):1,6.1:1):1);")
        node1 = "1.6"
        node2 = "10.7"
        self.assertTrue(self.speciesTreeA.nni(node1, node2).equals_structure(spr_tree))
        
        spr_tree = Tree.SpeciesTree("(((1.6:1,6.1:1):1,(10.7:1,5.8:1):1):1);")
        node1 = "10.7-5.8"
        node2 = "6.1"
        self.assertTrue(self.speciesTreeA.nni(node1, node2).equals_structure(spr_tree))
        
        self.assertTrue(self.speciesTreeA.equals(self.speciesTreeC))
    
    def test_possible_sprs(self):
        sprs = self.speciesTreeA.possible_sprs()
        self.assertEqual(len(sprs), 8)
        all_trees = [self.speciesTreeA]
        for spr in sprs:
            # Check that spr is unique
            self.assertEqual(sprs.count(spr), 1)
            # Check that spr trees are unique
            new_tree = self.speciesTreeA.spr(spr[0], spr[1]).standardize_branch_lengths()
            self.assertNotIn(new_tree, all_trees)
            all_trees.append(new_tree)
            
        sprs = self.speciesTreeB.possible_sprs()
        self.assertEqual(len(sprs), 156)
        all_trees = [self.speciesTreeB]
        for spr in sprs:
            # Check that spr is unique
            self.assertEqual(sprs.count(spr), 1)
            # Check that spr trees are unique
            new_tree = self.speciesTreeB.spr(spr[0], spr[1]).standardize_branch_lengths()
            self.assertNotIn(new_tree, all_trees)
            all_trees.append(new_tree)
            
    def test_possible_nnis(self):
        nnis = self.speciesTreeA.possible_nnis()
        self.assertEqual(len(nnis), 6)
        all_trees = [self.speciesTreeA]
        for nni in nnis:
            # Check that nni is unique
            self.assertEqual(nnis.count(nni), 1)
            self.assertEqual(nnis.count((nni[1], nni[0])), 0)
            # Check that nni trees are unique
            new_tree = self.speciesTreeA.nni(nni[0], nni[1]).standardize_branch_lengths()
            self.assertEqual(new_tree, self.speciesTreeA.nni(nni[1], nni[0]))
            self.assertNotIn(new_tree, all_trees)
            all_trees.append(new_tree)
            
        nnis = self.speciesTreeB.possible_nnis()
        self.assertEqual(len(nnis), 82)
        all_trees = [self.speciesTreeB]
        for nni in nnis:
            # Check that nni is unique
            self.assertEqual(nnis.count(nni), 1)
            self.assertEqual(nnis.count((nni[1], nni[0])), 0)
            
            # Check that nni trees are unique
            new_tree = self.speciesTreeB.nni(nni[0], nni[1]).standardize_branch_lengths()
            self.assertEqual(new_tree, self.speciesTreeB.nni(nni[1], nni[0]))
            self.assertNotIn(new_tree, all_trees)
            all_trees.append(new_tree)
    
if __name__ == '__main__':
    unittest.main()
