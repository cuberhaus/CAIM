clusters=(2 4 8 16 32 64 128)
n=${#clusters[@]}
for ((i = 0; i < $n; i++)); do
    c_size=${clusters[$i]}
    echo "python GeneratePrototypes.py --data documents$i$c_size.txt --nclust $c_size &"
    python GeneratePrototypes.py --data documents$i.txt --nclust $c_size &
done

wait
echo "Program ended successfully"
