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


## Implementation ##
The main logic for the Crank program lies in `Crank.py` with the main control loop 
`run_iteration()`.  `Crank.py` imports and uses several other files and packages:
- Cog.py
- Cogbox.py
- CrankStatistics.py
- GenesFile.py
- Job.py
- PyVM.py
- Scheduler.py
- Tree.py
- tests
- utilities
  - AlbertywScheduler.py
  - DarwinScheduler.py
  - GenesFileAnnotator.py
  - GenesFileComparison.py
  - GenesFileCreation.py
  - GenesFilePruner.py
  - GenesFileViz.py
  - LeafStripper.py
  - Reconcile.py
  - ReconcileSingle.py
  - RunTime.py
  - StatisticsVisualizer.py
  - TreeCompare.py
  - TreeVisulizer.py
Third party files/packages
- angst\_lib
- dendropy
- ete
- tree\_lib
System packages
- ?
### Dependencies ###

## Constraints and Pitfalls ##

