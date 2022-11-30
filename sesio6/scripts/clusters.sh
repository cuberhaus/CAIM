processes=()
clusters=(2 4 8 16 32 64 128)
n=${#clusters[@]}

python3 ExtractData.py --index abs --minfreq 0.1 --maxfreq 0.3 --numwords 200 --name 0 &
pid=$!
processes+=($pid)
trap 'kill ${processes[@]}' EXIT
wait
for ((i = 0; i < n; i++)); do
    c_size=${clusters[$i]}
    (set -x; python3 GeneratePrototypes.py --data documents0.txt --nclust "$c_size" &)
    pid=$!
    processes+=($pid)
done

trap 'kill ${processes[@]}' EXIT
wait
mkdir -p experiments/clusters
mv *.txt experiments/clusters/

wait
me=$(basename "$0")
echo "${me} ended successfully"
