IFS=$'\n'
array=`cat ../pair.list`

inDirec=/work/GoryaninU/mitsuki/mizuho/dna/row
outDirec=/work/GoryaninU/mitsuki/mizuho/dna/trim
for line in ${array[@]}
do 
    leftId=`echo ${line}|cut -d "," -f2`
    rightId=`echo ${line}|cut -d "," -f3`
    inLeft=${inDirec}/${leftId}.fastq.gz
    inRight=${inDirec}/${rightId}.fastq.gz
    outLeft=${outDirec}/${leftId}.fastq
    outRight=${outDirec}/${rightId}.fastq
    sbatch caller.sh ${inLeft} ${inRight} ${outLeft} ${outRight}
done
