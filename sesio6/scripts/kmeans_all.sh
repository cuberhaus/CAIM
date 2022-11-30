./scripts/cluster.sh
wait
./scripts/freq.sh
wait
./scripts/freq2.sh
wait
./scripts/size.sh
wait

./scripts/kmeans.sh -n size
wait
./scripts/kmeans.sh -n freq
wait
./scripts/kmeans.sh -n freq2
wait
./scripts/kmeans_cluster.sh
wait
