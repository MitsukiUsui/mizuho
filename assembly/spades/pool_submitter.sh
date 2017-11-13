array=(./yaml/anode.yaml ./yaml/chamber.yaml ./yaml/18m.yaml ./yaml/random.yaml)
for yaml in ${array[@]}
do
    basename=`basename ${yaml}`
    outDirec=/work/GoryaninU/mitsuki/out/spades/mizuho/${basename/.yaml/}
    sbatch pool.sh ${yaml} ${outDirec}
done
