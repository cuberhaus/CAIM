exp="clusters"
n=7
protos=($(ls experiments/$exp/ | cat | grep -i "prototype.*txt"))
docus=($(ls experiments/$exp/ | cat | grep -i "documents.*txt"))

for ((i = 0; i < n; i++)); do
    # echo "python generateprototypes.py --data documents$i.txt &"
    proto=${protos[$i]}
    docu=${docus[0]}
    echo "python3 ../MRKmeans.py  --prot ../experiments/$exp/$proto --docs ../experiments/$exp/$docu &"
    mkdir Kmeans_"$i"
    cd Kmeans_"$i"
    python3 ../MRKmeans.py  --prot ../experiments/$exp/$proto --docs ../experiments/$exp/$docu &
    cd ../
done

wait

mkdir Kmeans$exp/
mv Kmeans_* Kmeans$exp/
echo "Program ended successfully"
