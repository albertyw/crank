# Crank #

Phylogenetic tree reconstruction using AnGST (Analyzer of Gene and Species Trees)

## Purpose And Background ##
Crank is a program that finds the maximum parsimony species tree that fits a given 
set of gene trees.  Species and gene trees show how species and genes, 
respectively, evolved over the course of history.  More specifically, species 
trees show divergence events where species split, or speciated, while gene trees 
show speciations, losses (where genes ceased to exist), duplication (where genes
were duplicated in the same species), and horizontal gene transfer (where genes 
where transfered from one species to another).  Since gene trees are affected by 
many more events than species trees, and since gene trees do not always agree 
with each other, there is a problem in finding the "correct" species tree that 
best explains the speciation events in gene trees.  

The [AnGST algorithm](http://www.nature.com/nature/journal/v469/n7328/full/nature09649.html) 
is used by Crank to compute the parsimony of species/gene tree pairs.  The 
internals of the AnGST algorithm (and its implementation in Ranger DTL) are beyond 
the scope of this document but the output of AnGST generates a list of the 
simplest sequence of gene events needed for the gene tree to have arisen given 
the structure of the species tree.  While this was useful for analyzing 
patterns in gene history, this is used by Crank in reverse to analyze species 
history.  Crank uses the weighted average (the AnGST score) of gene events as a 
metric to evaluate species tree correctness.  

## Abstract Algorithm ##
Crank is essentially a relatively simple hill climbing algorithm that finds a 
(hopefully global, but probably local) min in species tree structure space where 
the score is the weighted average of the set of AnGST scores (i.e. Crank 
searches the species tree space for species trees that minimize the number of 
gene tree events required for the set of gene trees to have arisen from the 
species tree).  Starting from a single species tree and a set of gene trees from 
the species in the species tree, the Crank algorithm progresses as follows:

1.  The base species tree is reconciled using AnGST with the set of gene trees
2.  From the AnGST outputs, calculate the weighted average of AnGST scores 
and set that as the base score.  Also, count the frequency of each unique event 
predicted by AnGST.  
3.  Generate a list of tree operations - subtree prune and regraft (SPR), 
nearest neighbor interchange (NNI), and reroots - that should be tried on the 
base species tree.  SPRs are chosen based on the most frequent horizontal gene 
transfers.\*  NNIs are chosen by selecting random nodes, and reroots are chosen 
by rerooting on either child node of the base species tree's root.  
4.  Generate trial species trees based on the selected tree operations.  
5.  Reconcile each of the trial species trees with each of the gene trees.  
6.  Compute the AnGST score of each of the trial species trees
7.  Select the trees with AnGST scores lower than the base tree's and apply the 
operation(s) that created the tree(s) with the minimimum score(s) to the base tree.   
8.  If no operations were found, the algorithm has found a local minima.  Else, 
continue from step 1.  

### Running Time ###
Almost the entirety of the running time for Crank is waiting for AnGST to run.  
Therefore, the running time of Crank is highly dependent on how many gene trees 
are in the run dataset, the number of trial trees used, and the implementation of 
AnGST used (of which there is the original Python implementation and Ranger-DTL).  
The running time of the AnGST algorithm itself is mostly dependent on the number 
of the genes and species being reconciled.  

Since individual AnGST reconciliations are standalone and don't interact with 
each other, reconciliations are easily parallelizable.  Crank parallelizes the 
running of AnGST across several compute nodes through a built-in job scheduler.  
When run on the coyote cluster, one iteration of the AnGST algorithm can still 
take several hours to two days to complete, depending on the size of the dataset.  

## Input Data Generation ##
Since the input data are trees, they need to be generated from a list of species 
and the sequences of their gene families.  These can be generated in a variety 
of ways.  Currently, gene trees are generated from [arCOG](http://archaea.ucsc.edu/arcogs/) 
sequences.  

## Running Crank ##
Since Crank has a lot of files and configurable variables, there is a file in 
`utilities/Starter.py` which is used to hold Crank inputs and parameters.  See
that file for details about running Crank.  

### Crank Output ###
When you run Crank, you need to specify an output directory where Crank will 
place its output files.  The main output file is `output.txt`, which will show 
the summary results of the reconciliations of the the base tree and trial trees.  
There will also be a `shell` diretory and a `shell/finished` directory which 
holds the shell input files that run the reconciliations.  The `shell/finished` 
directory also contains the output of finished and crashed reconciliations.  The 
`stats` directory contains statistics computed by `CrankStatistics.py`.  

Each iteration of Crank creates a new subdirectory numbered by the iteration 
count.  In each iteration directory, there is a `base` subdirectory which contains
the input and output of the base tree's reconciliation, a `trial` subdirectory 
which contains the input and output of the trial trees' reconciliations, and 
a `trial_info` file which contains the operations used to create the trial trees.  

## Implementation ##
The main logic for the Crank program lies in `Crank.py` with the main control loop 
`run_iteration()`.  `Crank.py` imports and uses several other files and packages:
- Cog.py - A class that manages the reconciliation of a single species and 
  gene tree.  This also contains code to run AnGST (specifically Ranger-DTL) 
  and parse its output into Python variables.  
- Cogbox.py - A class that reads the parsed output of many Cog classes (several 
  gene trees, one species tree) and computes/holds summary data (e.g. scores, 
  run times, gene events)
- CrankStatistics.py - A class that computes and graphs higher level statistics 
  that aren't used within Crank.  
- GenesFile.py - A class that holds/reads/writes sets of gene trees
- Job.py - The script that is submitted to the compute cluster job queue to run 
  reconciliations.  
- PyVM.py - third party module to track memory usage
- Scheduler.py - Class that handles distributing/sending jobs to the cluster(s).  
  Handles submitting jobs to a local queue and sending jobs to other queues over 
  scp 
- Tree.py - Contains Tree (general tree reading/manipulation), SpeciesTree, and 
  GeneTree classes.  A lot of computation is actually handed off to ete package
- tests - directory containing very incomplete tests of Crank
    - TreeTest.py - actually relatively well tested
    - CogTest.py
- utilities
    - AlbertywScheduler.py - Receives jobs that have been copied from 
      Scheduler.py and runs them locally
    - DarwinScheduler.py - Receives jobs that have been copied from Scheduler.py
      and runs them on the local queue
    - GenesFileAnnotator.py - Annotates (adds comments) Genesfiles based on 
      configurable rules
    - GenesFileComparison.py - Compares gene trees between two GenesFiles and 
      computes some basic statistics
    - GenesFileCreation.py - Creates a GenesFile from a directory of individual 
      files
    - GenesFilePruner.py - a hackish script to select trees from one GenesFile 
      and save them to a new GenesFile
    - GenesFileViz.py - Creates an image of every tree in a GenesFile
    - LeafCounter.py - Counts the number of leaves in a GenesFile
    - LeafStripper.py - When reducing the number of species being analyzed, 
      remove leaves from species and gene trees (in GenesFiles) matching those 
      species
    - Reconcile.py - Manually reconcile a GenesFile against a species tree
    - ReconcileSingle.py - Manual reconcile a single gene tree against a species 
      tree
    - Starter.py - A file with configuration variables to start Crank running
    - StatisticsVisualizer.py - When run on a Crank output directory, creates 
      pretty graphs and tree images
    - TreeCompare.py - Compare the structure of two trees
    - TreeVisulizer.py - Converts a tree file into an image of the tree
    - leaf\_overlap - Finds coverage of different species by each tree in a 
      GenesFile
    
### Third party files/packages ###
- include
    - dtl - The Ranger-DTL executable implementation of AnGST
- ete - Another Tree manipulation package, forms the basis of Tree.py

### System packages ###
- matplotlib - Used by CrankStatistics to plot stats 
- [itol](https://github.com/albertyw/itol-api) - Used by CrankStatistics to 
  draw trees




[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/albertyw/crank/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

