#outDirec=/work/GoryaninU/mitsuki/out/fastqc/mizuho/dna/bin
outDirec=/home/m/mitsuki-usui/rsyncdir/files/fastqc/filter
while read line
do
    sbatch caller.sh ${line} ${outDirec}
done < filename.list
