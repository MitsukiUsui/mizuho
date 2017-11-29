numBins=173
for binId in `seq -f %03g 1 ${numBins}`
do
    if [ "$binId" = 003 ] || [ "$binId" = 006 ] || [ "$binId" = 085 ]; then
        echo "SKIP 3,6,85" 
    else
        binDirec=/work/GoryaninU/mitsuki/out/binning/distribute/bin${binId}
        left=${binDirec}/bin${binId}_R1.fastq
        right=${binDirec}/bin${binId}_R2.fastq
        outDirec=/work/GoryaninU/mitsuki/out/spades/mizuho/bin/bin${binId}
        sbatch single.sh ${left} ${right} ${outDirec}
        #echo "sbatch single.sh ${left} ${right} ${outDirec}"
    fi
done
