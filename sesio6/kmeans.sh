exp="size"
protos=($(ls experiments/$exp/ | cat | grep -i "prototype.*txt"))
docus=($(ls experiments/$exp/ | cat | grep -i "documents.*txt"))
n=6


for ((i = 0; i < n; i++)); do
    # echo "python generateprototypes.py --data documents$i.txt &"
    proto=${protos[$i]}
    docu=${docus[$i]}
    echo "python3 ../MRKmeans.py  --prot ../experiments/size/$proto --docs ../experiments/size/$docu &"
    mkdir Kmeans_"$i"
    cd Kmeans_"$i"
    python3 ../MRKmeans.py  --prot ../experiments/size/$proto --docs ../experiments/size/$docu &
    cd ../
done

wait

mkdir Kmeans/
mv Kmeans_* Kmeans/
echo "Program ended successfully"
