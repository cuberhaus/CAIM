processes=()
exp=""
TIMES=1                                  
usage() {                                 
    echo "Usage: $0 [ -n EXPERIMENT_NAME ]" 1>&2
}
exit_abnormal() {                         # Function: Exit with error.
    usage
    exit 1
}
#https://www.computerhope.com/unix/bash/getopts.htm
while getopts ":n:" options; do         # Loop: Get the next option;
    # use silent error checking;
    # options n and t take arguments.
    case "${options}" in                    #
        n)                                    # If the option is n,
            exp=${OPTARG}                     
            ;;
        :)                                    # If expected argument omitted:
            echo "Error: -${OPTARG} requires an argument."
            exit_abnormal                       # Exit abnormally.
            ;;
        *)                                    # If unknown (any other) option:
            exit_abnormal                       # Exit abnormally.
            ;;
    esac
done
if [[ $exp == "size" ]] ; then  
    n=6
fi
if [[ $exp == "freq" ]] ; then   
    n=5
fi
if [[ $exp == "freq2" ]] ; then   
    n=4
fi

# exp="size"
# n=6

# exp="freq"
# n=5

# exp="freq2"
# n=4

protos=($(ls experiments/$exp/ | cat | grep -i "prototype.*txt"))
docus=($(ls experiments/$exp/ | cat | grep -i "documents.*txt"))


for ((i = 0; i < n; i++)); do
    proto=${protos[$i]}
    docu=${docus[$i]}
    mkdir Kmeans_"$i"
    cd Kmeans_"$i"
    (set -x; python3 ../MRKmeans.py  --prot ../experiments/"$exp"/"$proto" --docs ../experiments/"$exp"/"$docu" &)
    pid=$!
    processes+=($pid)
    cd ../
done
trap 'trap " " SIGTERM; kill 0; wait; cleanup' SIGINT SIGTERM
wait

mkdir Kmeans"$exp"/
mv Kmeans_* Kmeans"$exp"/
mv Kmeans"$exp"/ experiments/Kmeans"$exp"/

wait
me=$(basename "$0")
#me="${me} $1"
echo "${me} ended successfully"
