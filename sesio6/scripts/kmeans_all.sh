# This command lines cannot be executed in parallel, because they are dependent on each other.
# Run elasticsearch:
# docker run -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.17.7
# Index the data:
# python3 IndexFiles.py --index abs --path arxiv_abs
./scripts/clusters.sh
./scripts/freq.sh
./scripts/freq2.sh
./scripts/size.sh

./scripts/kmeans.sh -n size
./scripts/kmeans.sh -n freq
./scripts/kmeans.sh -n freq2
./scripts/kmeans_cluster.sh
./scripts/results.sh
