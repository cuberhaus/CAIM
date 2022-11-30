n=6
for ((i = 0; i < n; i++)); do
    # echo "python generateprototypes.py --data documents$i.txt &"
    echo "python3 MRKmeans.py  --prot prototype"$i"_8.txt --docs documents0.txt &"
    mkdir Kmeans_"$i"
    cd Kmeans_"$i"
    python3 ../MRKmeans.py  --prot ../prototype"$i"_8.txt --docs ../documents0.txt &
    cd ../
done

wait

mkdir Kmeans/
mv Kmeans_* Kmeans/
echo "Program ended successfully"
