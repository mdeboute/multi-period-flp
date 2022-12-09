if [ $# -lt 2 ] || [ $# -gt 3 ]; then
    echo "Usage: ./benchmark.sh <data_dir> <algo> (<time_limit>)"
    echo "Where algo can be one of these: MIP, H"
    echo "<time_limit> is the time limit in seconds (default 600)."
    exit 1
fi

if [ $# -eq 3 ]; then
    time_limit=$3
else
    time_limit=600
fi

echo "Experimental Campaign:"
echo "Data directory: $1"
echo "Output directory: log/"
echo "Algorithm: $2"
echo "Time limit: $time_limit"

mkdir -p log
cd log && mkdir -p $2
echo `date` > $2/date.txt
cd ..

for instance in `ls $1` ; do
    echo "Resolution of $instance"
    python3 src/main.py $1/$instance $2 $time_limit > log/$2/log_${instance}

grep "Result" log/$2/*.txt >> log/$2/results_$time_limit.csv

exit 0