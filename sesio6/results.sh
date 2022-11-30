expf="Kmeanssize"
folders=($(ls $expf/ | cat | grep -i "kmeans.*"))

n=${#folders[@]}
for ((i = 0; i < n; i++)); do
    folder=${folders[$i]}
    protos=($(ls $expf/$folder | cat | grep -i "^prototypes.*.txt" ))

    m=${#protos[@]}
    k=$((m-1))
    proto=${protos[$k]}

    echo "python3 ProcessResults.py --prot $expf/$folder/$proto & > $expf/$folder/ProcessResults.txt"
    python3 ProcessResults.py --prot $expf/$folder/$proto & > $expf/$folder/ProcessResults.txt
done
wait
