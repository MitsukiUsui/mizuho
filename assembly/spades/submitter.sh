inDirec=/work/GoryaninU/mitsuki/mizuho/dna/trim

while read line
do
    sampleId=`echo ${line}|cut -d "," -f1`
    outDirec=/work/GoryaninU/mitsuki/out/spades/mizuho/${sampleId}
    left=${inDirec}/`echo ${line}|cut -d "," -f2`.fastq
    right=${inDirec}/`echo ${line}|cut -d "," -f3`.fastq
    sbatch single.sh ${left} ${right} ${outDirec}
done < ../../preprocess/pair.list
