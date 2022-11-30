exp="clusters"
n=7
protos=($(ls experiments/$exp/ | cat | grep -i "prototype.*txt"))
docus=($(ls experiments/$exp/ | cat | grep -i "documents.*txt"))

for ((i = 0; i < n; i++)); do
    proto=${protos[$i]}
    docu=${docus[0]}
    mkdir Kmeans_"$i"
    cd Kmeans_"$i"
    (
        set -x
        python3 ../MRKmeans.py --prot ../experiments/$exp/"$proto" --docs ../experiments/$exp/"$docu"
    ) &
    cd ../
done

wait

mkdir Kmeans$exp/
mv Kmeans_* Kmeans$exp/
mv Kmeans"$exp"/ experiments/Kmeans"$exp"/
echo "Program ended successfully"
