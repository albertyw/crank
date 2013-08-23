import os
import sys
import unittest

parent_path = os.path.dirname(os.path.realpath(__file__))+'/../'
sys.path.append(parent_path)
import Cog
import Tree

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        # Main Tree
        self.treeA = Tree.Tree("(((1.6:1.6,(10.7:10.7,5.8:5.8):1):2,6.1:6.1):3);")
        self.treeAgene = Tree.GeneTree("(10:1, 10:2, 1:3);")

        self.treeB = Tree.SpeciesTree("(>Censy:0.8058926132,(>Nitma:2.4197118915,((>Naneq:2.4823809221,(>Korcr:0.7730831714,(((>Metse:0.2559060825,((((>Sul14:2.92e-08,>SuliL:1e-10):0.0082212789,(>SuliM:0.0005938178,(>Sul27:2.85e-08,>Sul04:0.0011746087):5.84e-08):0.0110947563):0.0302607423,(>Sulso:0.0651170655,>Sul51:0.0233983025):0.035786701):0.1735174926,(>Sulto:0.1402264512,>Sulac:0.1821531309):0.1184812045):0.0839627931):0.4576303861,((>Stama:0.4959579683,>Deska:0.3326909102):0.2145933792,(>Aerpe:0.5677292816,(>Ignho:0.459713226,>Hypbu:0.4914945533):0.1132464597):0.0558979219):0.0521795622):0.0596234712,(>Thepe:0.5732554196,(>Calma:0.3648135352,(>Pyris:0.1089049421,(>Pyrae:0.0906121363,(>Pyrca:0.140830793,(>Thene:0.207139374,>Pyrar:0.1613356841):0.0825919492):0.0558812456):0.0505672118):0.332201978):0.1813495178):0.0774713355):0.0874261317):0.0343516883):0.0344254037,((>Picto:0.3443712778,(>Theac:0.1285664985,>Thevo:0.1292827663):0.1821867047):0.5024166574,(((>Theko:0.1036539487,(>Theon:0.0788987317,>Thega:0.0717925884):0.0551152173):0.0738557304,(>Thesi:0.109399163,(>Pyrab:0.1762393148,(>Pyrfu:0.0919377526,>Pyrho:0.0600342524):0.0678626143):0.0860137955):0.0347292589):0.342737983,((>Metka:0.5580446795,(((>Metfe:0.0905908203,(>Metja:0.0254059302,>Metvu:0.0862207584):0.0285842705):0.1148178512,(>Metae:0.1738164837,((>Metmp:0.0172843838,(>MetC6:0.0161202191,>MetmC:0.0199211135):0.0234923941):0.0179963735,(>Metva:0.1549900714,>MetC7:0.018313313):0.0734690166):0.156043704):0.1163127967):0.2616843311,(>Metth:0.2206592579,(>Metst:0.3888601327,>Metsm:0.2936778659):0.0760799086):0.2116156137):0.0663191915):0.0263460257,(>Arcfu:0.4234363207,((>Metsa:0.6107500188,(>Metbu:0.2992754794,(>Metba:0.0870442019,(>Metma:0.0400467482,>Metac:0.0385663683):0.0269549309):0.2565017687):0.0876674299):0.0856669712,((>Uncme:0.5132996842,(>Methu:0.2864439679,(>Metla:0.3321097823,(>Metbo:0.2513127008,(>Matpa:0.2068549504,>Metcu:0.1908209802):0.0439221196):0.0382028117):0.0639677678):0.2201573441):0.0488283041,(>Halut:0.2233196663,((>Halla:0.2396989584,>Natph:0.2316984331):0.0694239923,((>Halmu:0.1743917633,(>Halwa:0.253305379,>Halma:0.3620028661):0.0940959172):0.0395283765,(>Halsa:0.0150900792,>Halsp:0.0225698762):0.0150900792):0.0593159983):0.0641633086):0.4260961073):0.0520167438):0.0761500129):0.0615878781):0.068063798):0.0807388978):0.0297207559):1.7449886396):0.8058926132):0.01;")
        self.treeBgene = Tree.GeneTree("(((>Halma.55377613:0.178994,(>Halmu.257388946:0.212681,>Halla.222480477:0.456738):0.158186):0.173958,>Natph.76801488:0.550808):0.591830,>Halsp.15790704:0.000000,>Halsa.169236445:0.000000);")
        #self.treeBgene2 = Tree.GeneTree("((Halwa:1, Halma:1):1, Calma:1);")
        self.treeBgene2 = Tree.GeneTree("((Sul14:1, SuliL:1):1, (Halwa:1, Halma:1):1);")

        self.treeC = species_tree = Tree.SpeciesTree("((((((((Aerpe:1,(Hypbu:1,Ignho:1):1):1,(Deska:1,Stama:1):1):1,((Calma:1,((Pyrae:1,((Pyrar:1,Thene:1):1,Pyrca:1):1):1,Pyris:1):1):1,Thepe:1):1):1,Korcr:1):1,Naneq:1):1,((((Arcfu:1,(((((Halla:1,Natph:1):1,(((Halma:1,Halwa:1):1,Halmu:1):1,(Halsa:1,Halsp:1):1):1):1,Halut:1):1,(((((Matpa:1,Metcu:1):1,Metbo:1):1,Metla:1):1,Methu:1):1,Uncme:1):1):1,((((Metac:1,Metma:1):1,Metba:1):1,Metbu:1):1,Metsa:1):1):1):1,(((((((MetC6:1,MetmC:1):1,Metmp:1):1,(MetC7:1,Metva:1):1):1,Metae:1):1,(Metfe:1,(Metja:1,Metvu:1):1):1):1,((Metsm:1,Metst:1):1,Metth:1):1):1,Metka:1):1):1,(((Pyrab:1,(Pyrfu:1,Pyrho:1):1):1,Thesi:1):1,((Thega:1,Theon:1):1,Theko:1):1):1):1,((Metse:1,(((((Sul04:1,Sul27:1):1,SuliM:1):1,(Sul14:1,SuliL:1):1):1,(Sul51:1,Sulso:1):1):1,(Sulac:1,Sulto:1):1):1):1,(Picto:1,(Theac:1,Thevo:1):1):1):1):1):1,Nitma:1):1,Censy:1):1;")

    def test_init(self):
        species_tree = self.treeA
        genes_file_tree = dict({})
        genes_file_tree['name'] = 'asdf'
        genes_file_tree['weight'] = 1
        genes_file_tree['structure'] = str(self.treeAgene)
        genes_file_tree['boots'] = []
        penalties = dict({'hgt':3,'dup':2,'los':1,'spc':0})
        cog = Cog.Cog(species_tree, genes_file_tree, penalties)
        self.assertTrue(True)

    def test_reconcile(self):
        # Tree A
        species_tree = self.treeA
        genes_file_tree = dict({})
        genes_file_tree['name'] = 'asdf'
        genes_file_tree['weight'] = 1
        genes_file_tree['structure'] = str(self.treeAgene)
        genes_file_tree['boots'] = []
        penalties = dict({'hgt':3,'dup':2,'los':1,'spc':0})
        cog = Cog.Cog(species_tree, genes_file_tree, penalties)
        cog.reconcile()
        #self.assertNotEqual(cog.run_time, -1)
        self.assertEqual(cog.score, 3)
        self.assertEqual(cog.weighted_score, 3)
        self.assertEqual(cog.hgts, [])
        self.assertEqual(set(cog.events), set(['[brn]: 1-10-5', '[spc]: 1-10-5', '[cur]: 1', '[dup]: 10', '[cur]: 10', '[cur]: 10', '[los]']))

        # Tree B
        species_tree = self.treeB
        genes_file_tree = dict({})
        genes_file_tree['name'] = 'asdf'
        genes_file_tree['weight'] = 1
        genes_file_tree['structure'] = str(self.treeBgene2)
        genes_file_tree['boots'] = []
        cog = Cog.Cog(species_tree, genes_file_tree, penalties)
        cog.reconcile()

        #self.assertNotEqual(cog.run_time, -1)
        self.assertEqual(cog.score, 3)
        self.assertAlmostEqual(cog.weighted_score, 3.2753623188405796)
        self.assertEqual(cog.hgts, ['[hgt]: Sul14-SuliL --> Halwa-Halma'])
        self.assertEqual(cog.events, ['[brn]: Sul14-SuliL', '[hgt]: Sul14-SuliL --> Halwa-Halma', '[spc]: Halwa-Halma', '[cur]: Halma', '[cur]: Halwa', '[spc]: Sul14-SuliL', '[cur]: SuliL', '[cur]: Sul14'])
        #self.assertEquals(cog.events[0], '[brn]: Calma')

    def test_compute_hgt_weighted_score(self):
        angst_events = ['[spc]: Censy-Nitma-Naneq-Korcr-Metse-Sul14-SuliL-SuliM-Sul27-Sul04-Sulso-Sul51-Sulto-Sulac-Stama-Deska-Aerpe-Ignho-Hypbu-Thepe-Calma-Pyris-Pyrae-Pyrca-Thene-Pyrar-Picto-Theac-Thevo-Theko-Theon-Thega-Thesi-Pyrab-Pyrfu-Pyrho-Metka-Metfe-Metja-Metvu-Metae-Metmp-MetC6-MetmC-Metva-MetC7-Metth-Metst-Metsm-Arcfu-Metsa-Metbu-Metba-Metma-Metac-Uncme-Methu-Metla-Metbo-Matpa-Metcu-Halut-Halla-Natph-Halmu-Halwa-Halma-Halsa-Halsp', '[spc]: Nitma-Naneq-Korcr-Metse-Sul14-SuliL-SuliM-Sul27-Sul04-Sulso-Sul51-Sulto-Sulac-Stama-Deska-Aerpe-Ignho-Hypbu-Thepe-Calma-Pyris-Pyrae-Pyrca-Thene-Pyrar-Picto-Theac-Thevo-Theko-Theon-Thega-Thesi-Pyrab-Pyrfu-Pyrho-Metka-Metfe-Metja-Metvu-Metae-Metmp-MetC6-MetmC-Metva-MetC7-Metth-Metst-Metsm-Arcfu-Metsa-Metbu-Metba-Metma-Metac-Uncme-Methu-Metla-Metbo-Matpa-Metcu-Halut-Halla-Natph-Halmu-Halwa-Halma-Halsa-Halsp', '[los]: Naneq-Korcr-Metse-Sul14-SuliL-SuliM-Sul27-Sul04-Sulso-Sul51-Sulto-Sulac-Stama-Deska-Aerpe-Ignho-Hypbu-Thepe-Calma-Pyris-Pyrae-Pyrca-Thene-Pyrar-Picto-Theac-Thevo-Theko-Theon-Thega-Thesi-Pyrab-Pyrfu-Pyrho-Metka-Metfe-Metja-Metvu-Metae-Metmp-MetC6-MetmC-Metva-MetC7-Metth-Metst-Metsm-Arcfu-Metsa-Metbu-Metba-Metma-Metac-Uncme-Methu-Metla-Metbo-Matpa-Metcu-Halut-Halla-Natph-Halmu-Halwa-Halma-Halsa-Halsp', '[cur]: Nitma', '[dup]: Censy', '[cur]: Censy', '[hgt]: Censy --> Halla-Natph', '[dup]: Censy', '[cur]: Censy', '[cur]: Censy', '[dup]: Halla-Natph', '[spc]: Halla-Natph', '[hgt]: Natph --> Halma', '[cur]: Natph', '[cur]: Halma', '[cur]: Halla', '[spc]: Halla-Natph', '[hgt]: Natph --> Halmu', '[cur]: Natph', '[cur]: Halmu', '[hgt]: Halla --> Nitma', '[hgt]: Halla --> Halut', '[cur]: Halla', '[cur]: Halut', '[hgt]: Nitma --> Censy', '[cur]: Nitma', '[cur]: Censy']
        penalty_dict = dict({'hgt':3,'dup':2,'los':1,'spc':0})
        self.assertAlmostEqual(Cog.Cog.compute_hgt_weighted_score(angst_events, self.treeB, penalty_dict, 1), 25.52173913043478)
        angst_events = ['[hgt]: Halsp --> Censy']
        self.assertAlmostEqual(Cog.Cog.compute_hgt_weighted_score(angst_events, self.treeB, penalty_dict, 1), 3.1884057971014492)
        angst_events = ['[hgt]: Sul14 --> SuliL']
        self.assertAlmostEqual(Cog.Cog.compute_hgt_weighted_score(angst_events, self.treeB, penalty_dict, 1), 3.0144927536231885)
        angst_events = ['[hgt]: Halmu --> Halla']
        self.assertAlmostEqual(Cog.Cog.compute_hgt_weighted_score(angst_events, self.treeC, penalty_dict, 1), 3.0579710144927534)


if __name__ == '__main__':
    unittest.main()
