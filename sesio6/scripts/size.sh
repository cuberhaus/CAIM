sizes=(10 50 100 200 1000 10000)
n=${#sizes[@]}
for ((i = 0; i < n; i++)); do
    size=${sizes[$i]}
    echo "python ExtractData.py --index abs --minfreq 0.1 --maxfreq 0.3 --numwords $size --name $i &"
    python3 ExtractData.py --index abs --minfreq 0.1 --maxfreq 0.3 --numwords "$size" --name "$i" &
done
wait # This will wait for all child tasks to finish
for ((i = 0; i < n; i++)); do
    echo "python generateprototypes.py --data documents$i.txt &"
    # python GeneratePrototypes.py --data documents"$i".txt &
    python3 GeneratePrototypes.py --data documents"$i".txt --nclust 8 &
done
wait

mkdir -p experiments/size
mv *.txt experiments/size/
echo "Program ended successfully"
