# Load igraph library
library(igraph)

# Parameter p
p <- 10^(seq(-4,0,0.2))
# Clustering coefficient (transitivity)
trans <- c(1)
# Average path length
path <- c(1)

for(i in p)
{
  # Generate Watts-Strogatz graph
  watts <- watts.strogatz.game(1, 1000, 10, i)
  # Clustering coefficient (transitivity)
  trans <- c(trans, transitivity(watts))
  # Average path length
  path <- c(path, average.path.length(watts))
}

# Delete auxiliar values
trans <- trans[-1]
path <- path[-1]

# Normalized to be within the range [0, 1]
trans <- trans/trans[1]
path <- path/path[1]

# Plot the graph
plot(p, trans, ylim = c(0,1), log="x", ylab="coeff") 
points(p,path, pch=16)
