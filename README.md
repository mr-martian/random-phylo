# random-phylo
Experiments with random phylogenetic trees.

* [`gentree.py`](gentree.py)
Simulates a language family. Run as `gentree.py taxa change-rate`. `taxa` can be either a float indicating the probability of any particular taxon being output or an integer specifying the maximum number of taxa to be output (the simulation is not guaranteed to generate more than 2 taxa). Output is written to `random_tree.nex` and `random_matrix.nex`. Prints the final number of taxa.
* [`compare_reconstructions.R`](compare_reconstructions.R)
Apply phylogenetic algorithms to a matrix and compare it to a reference tree. Run as `compare_reconstructions.R tree matrix`. Both should be nexus files. Depends on packages `ape` and `phangorn`. Prints results as tab-separated list of method names and distances.
* [`run_iteration.sh`](run_iteration.sh)
Helper script. Runs `gentree.py` and `compare_reconstructions.R` a specified number of times. Run as `run_iteration.sh iterations taxa change-rate`. Writes results of each run to stdout in tsv format.
* [`clean_data.py`](clean_data.py)
* [`summarize_data.py`](summarize_data.py)
Helper scripts for processing output of `run_iteration.sh`. Both make assumptions about filenames.
* [`run_experiment.sh`](run_experiment.sh)
Wrapper script encoding an entire experiment.

