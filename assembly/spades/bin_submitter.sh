numBins=184
for binId in `seq -f %03g 1 ${numBins}`
do
    binDirec=/work/GoryaninU/mitsuki/out/binning/bin/bin${binId}
    left=${binDirec}/bin${binId}_R1.fastq
    right=${binDirec}/bin${binId}_R2.fastq
    outDirec=/work/GoryaninU/mitsuki/out/spades/mizuho/bin/bin${binId}
    sbatch single.sh ${left} ${right} ${outDirec}
done
