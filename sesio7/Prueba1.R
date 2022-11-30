# Load igraph library
library(igraph)
# Generate Watts-Strogatz graph
ws <- watts.strogatz.game(1, 100, 4, 0.05)
# Plot the graph
plot(ws, layout=layout.circle, vertex.label=NA, vertex.size=3)
# Clustering coefficient (transitivity)
transitivity(ws)
# Average path length
average.path.length(ws)

