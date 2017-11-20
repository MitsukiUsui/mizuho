#!/bin/bash

binDirec=${1}
outLeftFilepath=${2}
outRightFilepath=${3}
pairListFilepath="./list/pair.list"

echo ${binDirec},${outLeftFilepath},${outRightFilepath}
if [ -e ${outLeftFilepath} ]; then
    rm ${outLeftFilepath}
fi

if [ -e ${outRightFilepath} ]; then
    rm ${outRightFilepath}
fi

while read line
do
    left=`echo ${line}|cut -d "," -f2`
    right=`echo ${line}|cut -d "," -f3`
    inLeftFilepath=${binDirec}/`basename ${left}`
    inRightFilepath=${binDirec}/`basename ${right}`
    cat ${inLeftFilepath} >> ${outLeftFilepath}
    cat ${inRightFilepath} >> ${outRightFilepath}
done < ${pairListFilepath}
