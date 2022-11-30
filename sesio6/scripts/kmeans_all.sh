# This command lines cannot be executed in parallel, because they are dependent on each other.
./scripts/clusters.sh
./scripts/freq.sh
./scripts/freq2.sh
./scripts/size.sh

./scripts/kmeans.sh -n size
./scripts/kmeans.sh -n freq
./scripts/kmeans.sh -n freq2
./scripts/kmeans_cluster.sh
./scripts/results.sh
