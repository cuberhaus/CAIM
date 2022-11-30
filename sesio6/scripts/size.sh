processes=()

sizes=(10 50 100 200 1000 10000)
n=${#sizes[@]}
for ((i = 0; i < n; i++)); do
    size=${sizes[$i]}
    (set -x; python3 ExtractData.py --index abs --minfreq 0.1 --maxfreq 0.3 --numwords "$size" --name "$i" &)
    pid=$!
    processes+=($pid)
done
trap 'kill ${processes[@]}' EXIT
wait # This will wait for all child tasks to finish

for ((i = 0; i < n; i++)); do
    (set -x; python3 GeneratePrototypes.py --data documents"$i".txt --nclust 8 &)
    pid=$!
    processes+=($pid)
done
trap 'kill ${processes[@]}' EXIT
wait

mkdir -p experiments/size
mv *.txt experiments/size/
echo "Program ended successfully"
