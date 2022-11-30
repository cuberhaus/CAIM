# This command lines cannot be executed in parallel, because they are dependent on each other.
# Run elasticsearch:
# docker run -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.17.7
# Index the data:
# python3 IndexFiles.py --index abs --path arxiv_abs
./scripts/clusters.sh
#wait
./scripts/freq.sh
#wait
./scripts/freq2.sh
#wait
./scripts/size.sh
#wait

./scripts/kmeans.sh -n size
#wait
./scripts/kmeans.sh -n freq
#wait
./scripts/kmeans.sh -n freq2
#wait
./scripts/kmeans_cluster.sh
#wait
./scripts/results.sh
#wait
me=$(basename "$0")
echo "${me} ended successfully"
