exp=("Kmeanssize" "Kmeansclusters" "Kmeansfreq" "Kmeansfreq2")
n_exp=${#exp[@]}

for ((j = 0; j < n_exp; j++)); do
    expf=${exp[$j]}
    folders=($(ls $expf/ | cat | grep -i "kmeans.*"))

    n=${#folders[@]}
    for ((i = 0; i < n; i++)); do
        folder=${folders[$i]}
        protos=($(ls $expf/$folder | cat | grep -i "^prototypes.*.txt" ))

        m=${#protos[@]}
        k=$((m-1))
        proto=${protos[$k]}

        echo "(python3 processresults.py --prot $expf/$folder/$proto) > $expf/$folder/processresults.txt &"
        (python3 processresults.py --prot $expf/$folder/$proto) > $expf/$folder/processresults.txt &
    done
done

wait
