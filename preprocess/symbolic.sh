IFS=$'\n'
array=`tail -n +2 mizuho_metadata_dna.csv`

for line in ${array[@]}
do 
    filepath=`echo ${line}|cut -d "," -f2`
    sango=`echo ${line}|cut -d "," -f4`
    echo ${filepath},${sango}
    #ln -s ${sango} ${filepath}
done
