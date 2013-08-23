"""
This class reads data from Crank and visualizes the statistics and
"""

import os, shutil, sys, tempfile

sys.path.append('/home/albertyw/crank/src/')
import Tree

sys.path.append('../../itol')
sys.path.append(os.path.dirname(__file__)+'/../../itol')
import Itol, ItolExport

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pyplot


class CrankStatisticsVisualizer:
    """
    This program reads the output from CrankStatistics and creates charts
    from it
    """

    def __init__(self, output_directory):
        self.output_directory = output_directory
        self.stats_directory = self.output_directory+'/stats/'
        pass

    def file_lister(self, file_prefix):
        """
        For per iteration statistics, return a list of all the file locations
        that have been saved to
        """
        i = 0
        files = os.listdir(self.stats_directory)
        while i < len(files):
            if 'png' in files[i]:
                files.pop(i)
            elif file_prefix in files[i]:
                i += 1
            else:
                files.pop(i)
        files = [self.stats_directory+file_name for file_name in files]
        return files

    def xy_graph(self, file_name):
        """
        Read the input files as a list of (x coordinate, y coordinate)
        """
        file_handle = open(file_name, 'r')
        data = file_handle.read()
        file_handle.close()

        data = eval(data)
        x_axis = [item[0] for item in data]
        y_axis = [item[1] for item in data]
        pyplot.plot(x_axis, y_axis, 'ro')
        pyplot.title(file_name[file_name.rfind('/')+1:])
        pyplot.savefig(file_name+'.png')
        pyplot.clf()

    def xxi_graph(self, file_name):
        """
        Read the input files as a list of y coordinates, where the x coordinates
        are the index number
        """
        file_handle = open(file_name, 'r')
        data = file_handle.read()
        file_handle.close()

        data = list(eval(data))
        y_axis = data
        pyplot.plot(y_axis, 'ro')
        pyplot.title(file_name[file_name.rfind('/')+1:])
        pyplot.savefig(file_name+'.png')
        pyplot.clf()

    def triple_graph(self, file_name, label1, label2, label3):
        """
        Read the input files as three graphs (y1, y2, y3) where the x
        coordinates are the index number
        """
        file_handle = open(file_name, 'r')
        data = file_handle.read()
        file_handle.close()

        data = list(eval(data))
        y_axis0 = [item[0] for item in data]
        y_axis1 = [item[1] for item in data]
        y_axis2 = [item[2] for item in data]
        pyplot.subplot(111)
        pyplot.plot(y_axis0, 'r*', label=label1)
        pyplot.plot(y_axis1, 'bs', label=label2)
        pyplot.plot(y_axis2, 'g^', label=label3)
        pyplot.title(file_name[file_name.rfind('/')+1:])
        pyplot.legend()
        pyplot.savefig(file_name+'.png')
        pyplot.clf()

    def make_a_tree(self, tree, save_location):
        """
        Given a tree, render the tree using Itol and save to the save_location
        """
        # Format tree structure
        tree_structure = tree.tree_structure
        tree_structure = tree_structure.replace('>','')

        # Write tree structure to a tempfile
        temp = tempfile.NamedTemporaryFile()
        temp.write(tree_structure)
        temp.seek(0)
        temp.flush()

        # Upload to itol
        itol = Itol.Itol()
        itol.add_variable('treeFile',temp.name)
        itol.add_variable('treeName','asdf')
        itol.add_variable('treeFormat','newick')
        good_upload = itol.upload()
        if good_upload == False:
            print
            print 'ERROR:'+save_location
            print itol.comm.upload_output
            print
            return

        # Download from itol
        itol_exporter = itol.get_itol_export()
        itol_exporter.set_export_param_value('format','pdf')
        itol_exporter.set_export_param_value('ignoreBRL','1')
        itol_exporter.set_export_param_value('displayMode','normal')
        itol_exporter.set_export_param_value('fontSize','20')
        itol_exporter.export(save_location)
        temp.close()

    def make_graphs(self):
        """
        Convert the data into files
        """
        xy_graphs = ['leaves_vs_change_score','leaves_vs_score','leaves_vs_time']
        xxi_graphs = ['iteration_vs_time','iteration_vs_score','memory_vs_iteration']
        triple_graphs = [('better_operations_vs_iteration', 'nnis', 'sprs', 'reroots')]
        for category in xy_graphs:
            files = self.file_lister(category)
            for file_name in files:
                print file_name
                self.xy_graph(file_name)
        for category in xxi_graphs:
            files = self.file_lister(category)
            for file_name in files:
                print file_name
                self.xxi_graph(file_name)
        for graph in triple_graphs:
            category, label1, label2, label3 = graph
            files = self.file_lister(category)
            for file_name in files:
                print file_name
                self.triple_graph(file_name, label1, label2, label3)

    def make_trees(self):
        """
        Create trees from the base.tree outputs
        """
        # Make trees for each iteration
        csv_files = dict({})
        csv_files['/home/albertyw/tester/output/archaeal_groups.csv'] = 'groups'
        csv_files['/home/albertyw/tester/output/archaeal_phyla.csv'] = 'phyla'
        csv_files['/home/albertyw/tester/output/archaeal_species.csv'] = 'species'
        i = 1
        while os.path.exists(self.output_directory+'/'+str(i)+'/'):
            tree_location = self.output_directory+'/'+str(i)
            tree_handle = open(tree_location+'/base.tree','r')
            tree_string = tree_handle.read()
            tree_handle.close()
            tree = Tree.SpeciesTree(tree_string)
            self.make_a_tree(tree, tree_location+'/base.pdf')
            print tree_location+'/base.pdf'
            for file_location in csv_files.keys():
                renamed_tree = tree.rename_leaves(csv_file=file_location)
                if renamed_tree == tree:
                    continue
                self.make_a_tree(renamed_tree, tree_location+'/base_'+str(csv_files[file_location])+'.pdf')
                print tree_location+'/base_'+str(csv_files[file_location])+'.pdf'
            i += 1

        # Copy first and last trees
        i -=1
        shutil.copy(self.output_directory+'/1/base.pdf',\
            self.output_directory+'/Iteration1.pdf')
        print self.output_directory+'/Iteration1.pdf'
        shutil.copy(self.output_directory+'/'+str(i)+'/base.pdf',\
            self.output_directory+'/Iteration'+str(i)+'.pdf')
        print self.output_directory+'/Iteration'+str(i)+'.pdf'
        for file_location in csv_files.keys():
            try:
                shutil.copy(self.output_directory+'/1/base_'+str(csv_files[file_location])+'.pdf',\
                    self.output_directory+'/Iteration1_'+str(csv_files[file_location])+'.pdf')
                print self.output_directory+'/Iteration1_'+str(csv_files[file_location])+'.pdf'
            except:
                sys.exc_clear()
            try:
                shutil.copy(self.output_directory+'/'+str(i)+'/base_'+str(csv_files[file_location])+'.pdf',\
                    self.output_directory+'/Iteration'+str(i)+'_'+str(csv_files[file_location])+'.pdf')
                print self.output_directory+'/Iteration'+str(i)+'_'+str(csv_files[file_location])+'.pdf'
            except:
                sys.exc_clear()


if __name__ == "__main__":
    viz = CrankStatisticsVisualizer(sys.argv[1])
    viz.make_graphs()
    viz.make_trees()
