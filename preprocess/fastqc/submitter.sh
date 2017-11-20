outDirec=/work/GoryaninU/mitsuki/out/fastqc/mizuho/dna/bin
while read line
do
    sbatch caller.sh ${line} ${outDirec}
done < filename.list
