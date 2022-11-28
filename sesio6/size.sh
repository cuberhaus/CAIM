processes=()
python ExtractData.py --index news --minfreq 0.1 --maxfreq 0.3 --numwords 10000 --name 5 &
processes+=($!)
python ExtractData.py --index news --minfreq 0.1 --maxfreq 0.3 --numwords 1000 --name 4 &
processes+=($!)
python ExtractData.py --index news --minfreq 0.1 --maxfreq 0.3 --numwords 200 --name 3 &
processes+=($!)
python ExtractData.py --index news --minfreq 0.1 --maxfreq 0.3 --numwords 100 --name 2 &
processes+=($!)
python ExtractData.py --index news --minfreq 0.1 --maxfreq 0.3 --numwords 50 --name 1 &
processes+=($!)
python ExtractData.py --index news --minfreq 0.1 --maxfreq 0.3 --numwords 10 --name 0 &
processes+=($!)


# This method is a litle faster, or it should be since task could end at different times, so there are less bottlenecks
# echo "" > pid.txt # delete file
# for i in "${#processes[@]}"; do
#     echo "${processes[$i]}" >> pid.txt
#     wait ${processes[$i]}
#     python GeneratePrototypes.py --data documents$i.txt &
# done

wait # This will wait for all child tasks to finish

python GeneratePrototypes.py --data documents0.txt &
python GeneratePrototypes.py --data documents1.txt &
python GeneratePrototypes.py --data documents2.txt &
python GeneratePrototypes.py --data documents3.txt &
python GeneratePrototypes.py --data documents4.txt &
python GeneratePrototypes.py --data documents5.txt &

