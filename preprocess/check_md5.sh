IFS=$'\n'
array=`tail -n +2 rerun.list`

for line in ${array[@]}
do 
    google=`echo ${line}|cut -d "," -f5`
    sango=`echo ${line}|cut -d "," -f6`

    googleRet=`md5sum ${google}`
    googlemd5=`echo ${googleRet}|cut -d " " -f1`
    sangoRet=`md5sum ${sango}`
    sangomd5=`echo ${sangoRet}|cut -d " " -f1`
    
    if [ ${googlemd5} = ${sangomd5} ] ; then
        echo "o.k."
    else
        echo "fail"
        ls -alh ${google}
        ls -alh ${sango}
    fi
done
