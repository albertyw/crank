#! /usr/bin/env python

import dendropy

citation = """\
@article{HeathHH2012,
	Author = {Tracy A. Heath and Mark T. Holder and John P. Huelsenbeck},
	Doi = {10.1093/molbev/msr255},
	Journal = {Molecular Biology and Evolution},
	Number = {3},
	Pages = {939-955},
	Title = {A {Dirichlet} Process Prior for Estimating Lineage-Specific Substitution Rates.},
	Url = {http://mbe.oxfordjournals.org/content/early/2011/11/04/molbev.msr255.abstract},
	Volume = {29},
	Year = {2012}
	}
"""


dataset = dendropy.DataSet.get_from_string(
        "(A,(B,(C,(D,E))));",
        "newick")
dataset.annotations.add_citation(citation)
print dataset.as_string("nexml")
