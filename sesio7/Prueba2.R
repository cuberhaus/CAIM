# Load igraph library
library(igraph)
# Load edges.txt graph 
g <- read.graph("edges.txt", format="edgelist", directed=FALSE)

# 1.
# Plot the graph
plot(g, vertex.label=NA, vertex.size=3, layout=layout.kamada.kawai)
# Number of nodes
V(g)
# Number of edges
E(g)
# Diameter
diameter(g)
# Clustering coefficient (transitivity)
transitivity(g)
# Degree
degree(g)
# Degree Distribution
degree.distribution(g)
# Network with node sizes proportional to their pagerank
size_g=(page.rank(g)$vector)*500
plot(g,vertex.size=size_g)

# 2.

# Community detection
comm <- walktrap.community(g)
plot(comm, g)
# Nodes does the largest community found contain
max(sizes(comm))
# Plot the histogram of community sizes
plot(sizes(comm))

