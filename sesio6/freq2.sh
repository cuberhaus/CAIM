m_freq=(0.1,0.3 0.3,0.5 0.5,0.7 0.7,0.9)
n=${#sizes[@]} 

for i in ${m_freq[@]} ; do IFS=","; set $i;
    # freq=${m_freq[$i]}
    echo "python ExtractData.py --index news --minfreq $1 --maxfreq $2 --numwords 200 --name $i &"
    # python ExtractData.py --index news --minfreq $1 --maxfreq $2 --numwords 200 --name $i &
done

wait # This will wait for all child tasks to finish
# clusters=(2 4 8 16 32)
for ((i=0; i < $n; i++)); do
    echo "python generateprototypes.py --data documents$i.txt &"
    # python GeneratePrototypes.py --data documents$i.txt &
done

wait
echo "Program ended successfully"
