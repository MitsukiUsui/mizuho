numBins=173
for binId in `seq -f %03g 1 ${numBins}`
do
    outDirec=/work/GoryaninU/mitsuki/out/spades/mizuho/bin/bin${binId}
    seqFilepath=${outDirec}/scaffolds.fasta
    if [ -e ${seqFilepath} ]; then
        echo ${binId}" pass"
    else
        echo "ERROR: "${binId}", scaffolds.fasta does not exist."
    fi
done
