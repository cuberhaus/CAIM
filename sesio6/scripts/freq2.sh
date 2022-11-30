m_freq=(0.1,0.3 0.3,0.5 0.5,0.7 0.7,0.9)
n=${#m_freq[@]}
count=0
for i in ${m_freq[@]}; do
    IFS=","
    set $i
    echo "python ExtractData.py --index abs --minfreq $1 --maxfreq $2 --numwords 200 --name $count &"
    python3 ExtractData.py --index abs --minfreq "$1" --maxfreq "$2" --numwords 200 --name $count &
    count=$((count+1))
done

wait # This will wait for all child tasks to finish
# clusters=(2 4 8 16 32)
for ((i = 0; i < n; i++)); do
    echo "python generateprototypes.py --data documents$i.txt &"
    python3 GeneratePrototypes.py --data documents"$i".txt --nclust 8 &
    # python GeneratePrototypes.py --data documents"$i".txt &
done

wait
mkdir -p experiments/freq2
mv *.txt experiments/freq2/

echo "Program ended successfully"
