baseDirec=/work/GoryaninU/mitsuki/out/taxonomy
while read line
do
    assemname=`echo ${line}|cut -d "," -f1`
    assemDirec=${baseDirec}/${assemname}
    sbatch prodigal.sh ${assemDirec}
done < assembly.list
