listFilepath=${1}
baseDirec=${2}

while read line
do
    assemname=`echo ${line}|cut -d "," -f1`
    assemDirec=${baseDirec}/${assemname}
    sbatch prodigal.sh ${assemDirec}
done < ${listFilepath}
