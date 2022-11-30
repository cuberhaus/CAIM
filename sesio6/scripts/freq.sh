m_freq=(0.3 0.5 0.7 0.9 1)
n=${#m_freq[@]}
for ((i = 0; i < n; i++)); do
    freq=${m_freq[$i]}
    echo "python ExtractData.py --index abs --minfreq 0.1 --maxfreq $freq --numwords 200 --name $i &"
    python3 ExtractData.py --index abs --minfreq 0.1 --maxfreq "$freq" --numwords 200 --name "$i" &
done

wait # This will wait for all child tasks to finish
# clusters=(2 4 8 16 32)
for ((i = 0; i < n; i++)); do
    echo "python generateprototypes.py --data documents$i.txt &"
    python3 GeneratePrototypes.py --data documents"$i".txt --nclust 8 &
done

wait

mkdir -p experiments/freq
mv *.txt experiments/freq/
echo "Program ended successfully"
