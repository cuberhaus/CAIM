# Load igraph library
library(igraph)
# Load edges.txt graph 
g <- read.graph("edges.txt", format="edgelist")
# Plot the graph
plot(g, layout=layout.circle, vertex.label=NA, vertex.size=3)
# Clustering coefficient (transitivity)
transitivity(g)
# Average path length
average.path.length(g)
