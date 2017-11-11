IFS=$'\n'
array=`tail -n +2 mizuho_metadata_dna.csv`

for line in ${array[@]}
do 
    google=`echo ${line}|cut -d "," -f3`
    sango=`echo ${line}|cut -d "," -f4`

    googlemd5=`md5sum ${google}|cut -d " " -f1`
    sangomd5=`md5sum ${sango}|cut -d " " -f1`

    if [ ${googlemd5} = ${sangomd5} ] ; then
        echo "o.k."
    else
        echo "fail"
        echo "\t"${google},${sango}
    fi
done
