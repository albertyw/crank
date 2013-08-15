# Current Research Progress #

Crank has been an ongoing project since January 2009.  Since then, a lot of
search strategies have been tried in order to get a more plausible solution out
of Crank.  This is essentially a list of things that have been tried and their
effects.  If you haven't read it yet, you should read the README first.

## Simulated and Real Data ##
- **Incomplete sequences** - Should be very hard for Crank to reassemble the
species tree, but technically possible, as the AnGST algorithm will just
interpret missing genes as genetic deletions.  Has not been tested with simulated
or real data.
- **Starting with specific species trees** - Crank is pretty happy starting
from a species tree of any structure, though there are rare cases where
starting from a malformed species tree will result in Crank being stuck in a
local minima, rather than iterating to the correct tree.  Of course, Crank
converges on an answer much faster if the original species tree is closer to
the correct tree.  Randomized trees will work fine in smoother search
spaces (i.e. fewer gene event frequences).

## Simulated Data ##
- **High Gene Event Frequency** - Crank has been found to be relatively resistant to
simulated datasets with high gene event frequencies.  Crank is more sensitive to
datasets with high HGT and duplication but is much more resistant to high loss
frequencies.

## Real Data ##
- **Using bacterial species** - Using bacterial species should be a bad idea
because of the high amounts (and unequal distribution) of HGT between species.
The last time this was tested and confirmed was several years ago.
- **Using eukaryotic species** - Using eukaryotic species should result in
good results from Crank but kind of defeats the point of using something as
complex as the Crank algorithm because eukaryotes generally have extremely low
occurences of HGT.  Sequences from eukaryotic species have not been tested
with Crank and could possibly make a good sanity check.
- **Using different gene tree assembly methods** - In Summer 2011, raw brochier
sequences were aligned using both MUSCLE and FSA, with and without Gblocks, then
built into gene trees using PhyML.  Gblocks was found to have little effect on
Crank output.  MUSCLE was found to be a little better than FSA.  Good PhyML
settings were found to be very important to good Crank output.  See PhyML
settings below.
- **Adding bootstraps into AnGST** - This was tried also in Summer 2011 but was
found to result in negligible improvements to Crank but with drastically slower
computation.
- **Using subsets of gene trees** - See Weighting Gene Trees Differently
- **Using only subsets species from each class of Archaea** - Crank has proven to
be very good at grouping classes of Archaeal species together.  Therefore, in
order to lessen compute time, multiple species in classes can be pruned in order
to decrease data and therefore compute time.

## General Search Strategies ##
- **Depth first search** - Very early on, a depth first search was tried but it
was extremely inaccurate.  The search would apply the most common HGT as an SPR.
- **Reversing SPR direction** - HGTs are supposed to be "solved" by pruning the
gene acceptor node and grafting it to the gene donor node.  The reverse was tried
on accident (moving the gene donor node to the gene acceptor node) which resulted
in worse, but not very bad results.
- **Nearest Neighbor Interchange** - Randomly chosen nodes are switched and
tested at each iteration.  This greatly helps with getting Crank to converge at
a more probable tree because it effectively increases entropy in the search and
therefore allows Crank to get out of local minima, as well as possibly reducing
overall compute time.
- **Tree Rerooting Through Single Rotation** - At every iteration, Crank will
try rotating the tree (i.e. reroot the tree on each of the root's direct child
nodes) to try two more trees.  This helps to solve problems with incorrect tree
rooting but is still very suseptible to falling into local minima (or even
having the correct tree be less desirable than an incorrectly rooted tree)
- **Exhaustive Tree Rerooting Search** - It may be useful to try testing species
trees that have been rooted at every single node of the original tree.  This may
help with getting out of local minima at moderate computational cost (number of
nodes increases linearly to number of leaves in the tree)
- **Exhaustive Search** - Though this would get the search out of local mins,
the number of possible tree structures rises non polynomially against number of
leaves.  This would only be practically plausible for very small trees.
- **Iteratively Adding Species** - Another strategy which has not been tested
yet is iteratively adding species into species trees, testing the species tree
with every possible grafting.  This would effectively limit the size of trees
that can be built, but would also effectively test every possible tree structure.
This has yet to be explored.
- **Heuristic to increase search space at later iterations** - It would be
interesting to increase the search space (i.e. the number of NNIs, SPRs, and reroots)
at later iterations in order to keep Crank from falling into local minima.  This
would be at the expense of computational time.  This has not been tested
- **Search backtracking** - Especially in early iterations of Crank, the search
will find many possible changes to the species tree to decrease the Crank score and
thereby increase confidence in the species tree.  Since some of these changes may
conflict, Crank will only apply the best and second best change and use the
resultant species tree for future iterations.  It would be good to have Crank
try backtracking and seeing what the skipped paths result in.
- **Penalizing loss/duplication events** - The Crank algorithm only tries
SPRs based on HGT events.  Loss and Duplication events are ignored, except for
calculating overall tree scores.  There should be some way of Crank using loss
and duplication event data.  It can be direct (e.g. a loss for a species
moves that species out of its clade) or indirect (e.g. a loss decreases the
confidence in the gene tree, and thereby possibly the gene tree's weight?).

## Run Parameters ##
- **Increasing Depth of Search** - Since in general Crank runs until the tree is
converged, increasing the depth of the breadth-first Crank algorithm, is a moot
point.
- **Increasing SPRs Tested** - This has been looked into quite a bit.  There is a
loose but significant correlation between good SPRs and the prevalence of their
related HGTs.  Increasing SPRs would test HGTs with lower prevalence so therefore
there would be less return.
- **Increasing NNIs Tested** - Since NNIs are chosen and tested randomly, increasing
the number of NNIs tested should increase the accuracy of Crank.  However, at later
iterations of Crank, NNIs are less useful.
- **Weighting Gene Trees Differently** -
  - Weighting by number of unique leaves (number of species)
  - Weighting by number of leaves (number of genes)
  - Weighting by `(species)/avg(number of leaves per species)`
  All of these, particularly the unique leaves weighting have a slight positive
  effect on the accuracy of Crank.  However, the effect is very small and
  multiplying the weight has a negative effect on Crank.
  - Using only ribosomal trees
  Using only ribosomal gene trees, or just the 16S tree, results in Crank running
  very fast, and the results are typical of other studies that only use ribosomal
  trees.  A better way may be creating a weighting strategy that naturally
  heavily weight ribosomal trees, though I haven't been able to find one yet.
  - Using only certain types of genes
  Some genes are believed to inherently have high HGT potential (e.g. defense genes)
  while other genes have lower potential (e.g. metabolic genes).  Weighting gene
  trees by their inferred type may be useful, but has yet to be explored.
- **Calculating summary AnGST Score Differently** - AnGST scores are not normally
distributed.  Currently Crank takes the mean AnGST score, which may not
accurately represent the score of all the reconciliations.  Perhaps a median
would be better?
- **Changing gene event penalties for AnGST** - This was tried a bit, but the
default penalties (hgt:3, dup:2, los:1, spc:0) work pretty well.  Greatly modifying
gene event penalties hasn't been tested (nor is it expected to work well).


## Estimating Tree Confidence ##
- **Comparing Average AnGST Scores**
- **Number of gene trees covering each species**
- **Number of gene trees coving each pair of species**
- **Number of gene trees overall**
- **Comparing resultant species trees against published trees**
- **Perturbing the converged tree and seeing how much the score increases** -
If the score increases a lot, then there would be more confidence in the current
tree.


## PhyML Settings ##
These are the rough PhyML settings that have resulted in the best gene trees for Crank
```
data_type = '1'
format = 's'
data_sets = '1'
bootstrap_sets = '10'
model = 'WAG'
invar = 'e'
nb_categ = '4'
alpha = 'e'
tree = 'BIONJ'
opt_topology = 'y'
opt_lengths = 'n'
```
