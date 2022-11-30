processes=()
m_freq=(0.1,0.3 0.3,0.5 0.5,0.7 0.7,0.9)
n=${#m_freq[@]}
count=0
for i in ${m_freq[@]}; do
    IFS=","
    set $i
    (set -x; python3 ExtractData.py --index abs --minfreq "$1" --maxfreq "$2" --numwords 200 --name $count &)
    pid=$!
    processes+=($pid)
    count=$((count+1))
done
#trap 'kill ${processes[@]}' SIGINT
trap 'trap " " SIGTERM; kill 0; wait; cleanup' SIGINT SIGTERM
wait # This will wait for all child tasks to finish
# clusters=(2 4 8 16 32)
for ((i = 0; i < n; i++)); do
    (set -x; python3 GeneratePrototypes.py --data documents"$i".txt --nclust 8 &)
    pid=$!
    processes+=($pid)
done
#trap 'kill ${processes[@]}' SIGINT
trap 'trap " " SIGTERM; kill 0; wait; cleanup' SIGINT SIGTERM
wait

mkdir -p experiments/freq2
mv *.txt experiments/freq2/

wait
me=$(basename "$0")
echo "${me} ended successfully"
