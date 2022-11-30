# if the number of arguments is less than 3 or greater than 4, print the usage
if [ $# -lt 3 ] || [ $# -gt 4 ]; then
    echo "Usage: ./benchmark.sh <data_dir> <sol_dir> <algo> (<time_limit>)"
    echo "Where algo can be one of these: MIP, H"
    echo "<time_limit> is the time limit in seconds (default 600)."
    exit 1
fi

echo Experimental Campaign:
echo Data directory: $1
echo Output directory: $2
echo Algorithm: $3
echo Time limit: $4

# if the user provides a time limit, use it
if [ $# -eq 4 ]; then
    time_limit=$4
else
    time_limit=600
fi

algo_dir="${3#*--}"
mkdir -p $2  # create the output directory if it does not already exist
cd $2 && mkdir -p $algo_dir
echo `date` > $algo_dir/date.txt
cd ..

for instance in `ls $1` ; do  # for each instance in directory $1
    echo Resolution of $instance
    python3 src/main.py $1/$instance $3 $time_limit >> $2/$algo_dir/log_${instance} # writing console output to a log file
done

grep "Result" $2/$algo_dir/*.txt >> $2/$algo_dir/results.csv  # lines containing the word "Result" will be concatenated in the results.csv file

exit 0