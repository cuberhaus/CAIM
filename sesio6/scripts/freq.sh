processes=()
m_freq=(0.3 0.5 0.7 0.9 1)
n=${#m_freq[@]}
for ((i = 0; i < n; i++)); do
    freq=${m_freq[$i]}
    (set -x; python3 ExtractData.py --index abs --minfreq 0.1 --maxfreq "$freq" --numwords 200 --name "$i" &)
    pid=$!
    processes+=($pid)
done
#trap 'kill ${processes[@]}' SIGINT
trap 'trap " " SIGTERM; kill 0; wait; cleanup' SIGINT SIGTERM
wait # This will wait for all child tasks to finish

for ((i = 0; i < n; i++)); do
    (set -x; python3 GeneratePrototypes.py --data documents"$i".txt --nclust 8 &)
    pid=$!
    processes+=($pid)
done
#trap 'kill ${processes[@]}' SIGINT
trap 'trap " " SIGTERM; kill 0; wait; cleanup' SIGINT SIGTERM
wait

mkdir -p experiments/freq
mv *.txt experiments/freq/

wait
me=$(basename "$0")
echo "${me} ended successfully"
