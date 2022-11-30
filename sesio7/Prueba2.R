# Load igraph library
library(igraph)
# Load edges.txt graph 
g <- read.graph("edges.txt", format="edgelist")
# Plot the graph
plot(g, vertex.label=NA, vertex.size=3)
# Number of nodes
V(g)
# Number of edges
E(g)
# Diameter
diameter(g)
# Clustering coefficient (transitivity)
transitivity(g)
# Degree Distribution
degree.distribution(g)

