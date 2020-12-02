#!/usr/bin/env Rscript

args = commandArgs(trailingOnly=TRUE)

if(length(args) < 2) {
  stop("Must pass in 2 .nexus files [tree, matrix].", call.=FALSE)
}

library(ape)
library(phangorn)

tree.ref.full <- read.nexus(args[1])
data <- read.nexus.data(file = args[2])
data.phydata = phyDat(as.data.frame(data), format="NEXUS", type="USER",
                             levels=c(0,1,2,3,4,5,6,7,8,9,"-"))

data.dist = dist.ml(data.phydata)

# Neighbor Joining
tree.nj = NJ(data.dist)

pars.nj = parsimony(tree.nj, data.phydata)
tree.nj.optim = optim.parsimony(tree.nj, data.phydata, trace=0)

# UPGMA
tree.upgma = upgma(data.dist)

pars.upgma = parsimony(tree.upgma, data.phydata)
tree.upgma.optim = optim.parsimony(tree.upgma, data.phydata, trace=0)

# Maximum Likelihood
fit = pml(unroot(tree.upgma), data=data.phydata)
fit2 = update(fit, k=4, inv=0.2)
fit3 = optim.pml(fit2, model="GTR", optInv=TRUE, optGamma=TRUE, rearrangement = "NNI", control = pml.control(trace = 0))
tree.ml = fit3$tree

# distances
printdist <- function(name, ref, comp) {
  distance = dist.topo(ref, unroot(comp))
  cat(paste(name, distance, "", sep="\t"))
}
tree.ref <- unroot(drop.tip(tree.ref.full, setdiff(tree.ref.full$tip.label, tree.nj$tip.label)))
printdist("NJ", tree.ref, tree.nj)
printdist("NJ parsimony", tree.ref, tree.nj.optim)
printdist("UPGMA", tree.ref, tree.upgma)
printdist("UPGMA parsimony", tree.ref, tree.upgma.optim)
printdist("ML", tree.ref, tree.ml)
cat("\n")

