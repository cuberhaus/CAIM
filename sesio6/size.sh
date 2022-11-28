sizes=(10 50 100 200 1000 10000)
n=${#sizes[@]}
for ((i = 0; i < $n; i++)); do
    size=${sizes[$i]}
    echo "python ExtractData.py --index news --minfreq 0.1 --maxfreq 0.3 --numwords $size --name $i &"
    python ExtractData.py --index news --minfreq 0.1 --maxfreq 0.3 --numwords $size --name $i &
done

wait # This will wait for all child tasks to finish
# clusters=(2 4 8 16 32)
for ((i = 0; i < $n; i++)); do
    echo "python generateprototypes.py --data documents$i.txt &"
    python GeneratePrototypes.py --data documents$i.txt &
done

wait
echo "Program ended successfully"
