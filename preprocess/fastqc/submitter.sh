outDirec=/work/GoryaninU/mitsuki/out/fastqc/mizuho/dna/trim
while read line
do
    sbatch caller.sh ${line} ${outDirec}
done < filename.list
