#!/bin/bash
#SBATCH -p short,debug
#SBATCH --time=0-00:05:00
#SBATCH -o iotest.out

mypid=$$
echo 'My pid is '$mypid
echo "I'm running at "$HOSTNAME

module load anaconda3

for datafile in $(ls data/inputmatrix*.dat | sort); do
	datanumber=$(echo $datafile | cut -d '_' -f 2)
	srun strace -c -e trace=file python `dirname $0`/analyze_iodata.py --input $datafile --output 'data/outputmatrix_'$datanumber
done

echo 'Disk operations done:'
cat /proc/$mypid/io
